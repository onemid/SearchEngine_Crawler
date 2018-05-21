import distributor


if __name__ == '__main__':

    dist = distributor.Distributor(need_checkpoint=True,
                                   need_db_log=False,
                                   need_es_store=True,
                                   need_source_store=False,
                                   need_parsed_store=False)
    dist.dispatcher()
