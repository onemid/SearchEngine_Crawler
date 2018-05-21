import configparser


class Config():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config/basic_settings.ini')

        self.urls = config.get('BASIC_SETTINGS', 'urls', raw=False)
        self.urls = self.urls.split(",")
        self.render = config.get('BASIC_SETTINGS', 'render', raw=False)
        self.encoding = config.get('BASIC_SETTINGS', 'encoding', raw=False)
        self.workers = int(config.get('BASIC_SETTINGS', 'workers', raw=False))
        self.max_depth = int(config.get(
            'BASIC_SETTINGS', 'max_depth', raw=False))

        self.storage_loc = config.get('STORAGE', 'storage_location', raw=False)
        self.parsed_storage_loc = config.get(
            'STORAGE', 'parsed_storage_location', raw=False)
        self.db_loc = config.get('STORAGE', 'db_location', raw=False)
        self.checkpoint_loc = config.get(
            'STORAGE', 'chk_pt_location', raw = False)
            
        self.es_index = config.get(
            'ELASTICSEARCH', 'index', raw=False)
        self.es_doc_type = config.get(
            'ELASTICSEARCH', 'doc_type', raw=False)

        self.config_rule = configparser.ConfigParser()
        self.config_rule.read('./config/url_filter.ini')

        self.exc_rules = self.config_rule.get(
            'EXCLUSION', 'exclusion', raw=False)
        self.exc_rules = self.exc_rules.split(",")

        self.inc_rules = self.config_rule.get(
            'INCLUSION', 'inclusion', raw=False)
        self.inc_rules = self.inc_rules.split(",")

        self.empty = ''
