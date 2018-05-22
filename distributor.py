import multiprocessing as mp
import dnsresolver
import httpfetcher
import linkextractor
import urlseen
import logger
import store
import urlfilter
import checkpoint
import os.path
import pickle
import sys
import datetime
import config
import contentparser
import time


class Distributor():
    def __init__(self,
                 need_checkpoint=True,
                 need_db_log=True,
                 need_es_store=True,
                 need_source_store=True,
                 need_parsed_store=True):
        cfg = config.Config()
        self.__workers = cfg.workers
        # self.__urls = cfg.urls
        self.__terminate = False
        self.__dud = urlseen.DupURLDel()
        self.__title_seen = urlseen.DupURLDel()
        self.__urls = set(cfg.urls)
        self.__finished_urls = set()
        self.__render = cfg.render
        self.__max_depth = cfg.max_depth

        self.__need_checkpoint = need_checkpoint
        self.__need_db_log = need_db_log
        self.__need_es_store = need_es_store
        self.__need_parsed_store = need_parsed_store
        self.__need_source_store = need_source_store

        self.__storage = cfg.storage_loc
        self.__db = cfg.db_loc
        self.__checkpoint = cfg.checkpoint_loc
        self.__content_parsed = cfg.parsed_storage_loc
        self.__es_index = cfg.es_index
        self.__es_doc_type = cfg.es_doc_type

        self.__inc_rules = cfg.inc_rules
        self.__exc_rules = cfg.exc_rules
        self.__encoding = cfg.encoding
        self.__chkpt = checkpoint.Checkpoint(self.__checkpoint, self.__db)

        if self.__need_checkpoint:
            assert self.__checkpoint != '', '[!] You need to supply checkpoint location in config file'
        if self.__need_db_log:
            assert self.__db != '', '[!] You need to supply db location in config file'
        if self.__need_es_store:
            assert self.__es_index != '', '[!] You need to supply es index in config file'
            assert self.__es_doc_type != '', '[!] You need to supply es doc_type in config file'
        if self.__need_parsed_store:
            assert self.__content_parsed != '', '[!] You need to supply parsed file location in config file'
        if self.__need_source_store:
            assert self.__storage != '', '[!] You need to supply page source file location in config file'

    def dispatcher(self):

        if self.__need_checkpoint and os.path.isfile(self.__checkpoint + '/pending_urls.chkpt'):
            print('[i] Previous Work Stage Found')
            tmp_urls = self.__chkpt.recover('/pending_urls.chkpt')
            tmp_urls_seen = self.__chkpt.recover('/urls_seen.chkpt')
            tmp_title_seen = self.__chkpt.recover('/title_seen.chkpt')
            self.__urls = tmp_urls if len(tmp_urls) else self.__urls
            self.__dud = urlseen.DupURLDel(
                tmp_urls_seen) if len(tmp_urls_seen) else urlseen.DupURLDel()
            self.__title_seen = urlseen.DupURLDel(
                tmp_title_seen) if len(tmp_title_seen) else urlseen.DupURLDel()
        elif not self.__need_checkpoint:
            print('[i] Checkpoint Features Disabled')
        else:
            print('[i] Previous Work Stage Not Found; Using Default')

        depth = 1

        while not self.__terminate:
            print('======= Depth: %d / %d =======' % (depth, self.__max_depth))
            print('[>] %s URL(s) to process\r' % (len(self.__urls)))
            start_time = time.time()
            p = mp.Pool(processes=self.__workers)
            reps = p.map(self._job, (i for i in enumerate(self.__urls)))

            with open('/home/garygone/flowoverstack/crawler/log.txt', "a+") as f:
                f.write('======= Depth: %d / %d =======\n' %
                        (depth, self.__max_depth))
                f.write('[>] %s URL(s) to process\n' % (len(self.__urls)))

            self.__urls = set()

            for rep in reps:
                # print(rep["seen"])
                self.__dud.add_to_urls_seen(rep["seen"])
                self.__dud.add_to_urls_seen(rep["seen_new"])

            for rep in reps:
                after_verify_urls = urlfilter.URLFilter(
                    self.__dud.verify_seen_filter(rep["result"]), self.__exc_rules, self.__inc_rules)
                after_verify_urls = after_verify_urls.filter()
                self.__urls = self.__urls.union(after_verify_urls)

            end_time = time.time()

            with open('./log.txt', "a+") as f:
                f.write('Time:' + str(end_time - start_time) + '\n')

            if self.__need_checkpoint:
                self.__chkpt.store(self.__urls, '/pending_urls.chkpt')
                self.__chkpt.store(
                    self.__dud.get_urls_seen(), '/urls_seen.chkpt')

            depth += 1
            p.close()
            p.join()
            if depth > self.__max_depth or self.__urls == set():
                self.__terminate = True

    def _job(self, url):
        idx, url = url
        sys.stdout.write("\033[K")
        sys.stdout.write('[*] Processing [#%d]: %s\r' % (idx, url))
        sys.stdout.flush()
        # drl = dnsresolver.DNSResolver()
        hf = httpfetcher.HTTPFetcher(url, self.__encoding, self.__render)
        page_source, status_code, new_url = hf.fetch_page()
        ler = linkextractor.LinkExtractor(new_url)
        result = ler.parse_page_links(page_source)

        if status_code != 429:
            if page_source != '':

                cnt_paser = contentparser.ContentParser()
                cnt_result = cnt_paser.content_parsing(page_source)

                if not self.__title_seen.check_if_seen(cnt_result["title"]):

                    if self.__need_source_store:
                        storage = store.Store(self.__storage, new_url)
                        storage.store(page_source)

                    if self.__need_parsed_store:
                        cnt_storage = store.Store(
                            self.__content_parsed, new_url)
                        content_to_store = ''
                        for key, value in cnt_result.items():
                            content_to_store += '@' + \
                                str(key) + ':' + str(value) + '\n'
                        cnt_storage.store(content_to_store)

                    if self.__need_es_store:
                        cnt_result["url"] = new_url
                        cnt_result["links"] = len(result)
                        es_storage = store.Store()
                        es_storage.store_to_es(
                            self.__es_index, self.__es_doc_type, cnt_result)

                    # self.__title_seen.add_to_urls_seen(cnt_result["title"])

            # self.__dud.add_to_urls_seen(url)
            # self.__dud.add_to_urls_seen(new_url)
            # self.__urls.remove(url)

            if self.__need_db_log:
                log = logger.Logger(self.__db + '/url_seen')
                log.log_seen(url)
                log.log_seen(new_url)

            # if self.__need_checkpoint and idx % 10 == 0:
            #     print('[@] Saving Checkpoint [%s]............................\r' % (
            #         str(datetime.datetime.now())))
            #     self.__chkpt.store(self.__urls, '/pending_urls.chkpt')
            #     self.__chkpt.store(
            #         self.__dud.get_urls_seen(), '/urls_seen.chkpt')
            #     self.__chkpt.store(
            #         self.__title_seen.get_urls_seen(), '/title_seen.chkpt')

        return {'result': result, 'status_code': status_code, 'seen': url, 'seen_new': new_url}
