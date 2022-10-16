import datetime
import logging
import os
import __main__
import inspect
import json

class LogManager() :
    '''
    ログ管理クラス
    '''
    def __init__(self,setting_file_path_json=''):
        '''
        コンストラクタ

        Parameters
        ----------
        setting_file_path_json:str 
            json設定ファイルのフルパス
        '''
        self.filename = self.__create_log_path()
        stdout = False
        level_str = 'INFO'
        if setting_file_path_json != '':
            config = None
            with open(setting_file_path_json) as f:
                config = json.load(f)
            if config is not None:
                self.filename = config['output_filepath']
                if config['stdout'] == 'True':
                    stdout = True
                level_str = config['loglevel']
        self.format = '%(levelname)s [%(asctime)s] %(message)s'
        #ロガーを生成
        dirnames=os.path.dirname(__main__.__file__).split('\\')
        logger_name = dirnames[len(dirnames)-1] + '.' + os.path.basename(__main__.__file__).replace('.py','')
        self.logger = logging.getLogger(logger_name)

        #ログレベルを設定
        self.__setLevel(level_str)

        #ハンドラを登録
        self.__set_handler(self.filename,self.format,stdout)
    
    def info(self,message):
        '''
        ログに情報メッセージを出力する
        '''
        self.logger.info(self.__get_file_name_and_line_no_caller()+message)
    
    def error(self,message):
        '''
        ログにエラーメッセージを出力する
        '''
        self.logger.error(self.__get_file_name_and_line_no_caller()+message)
        
    def warning(self,message):
        '''
        ログに警告メッセージを出力する
        '''
        self.logger.warning(self.__get_file_name_and_line_no_caller()+message)
    
    def debug(self,message):
        '''
        ログにデバッグメッセージを出力する
        '''
        self.logger.debug(self.__get_file_name_and_line_no_caller()+message)

    def critical(self,message):
        '''
        ログにクリティカルメッセージを出力する
        '''
        self.logger.critical(self.__get_file_name_and_line_no_caller()+message)
    
    def __set_handler(self,filename,format,stdout):
        '''
        ハンドラの登録
        
        Parameters
        ----------
        filename:str 
            ログファイルのフルパス
        format:str
            ログの出力フォーマット
        stdout:bool
            ログを標準出力に表示するか否かの設定 
        '''
        #登録ハンドラー初期化
        for h in self.logger.handlers[:]:
            self.logger.removeHandler(h)
            h.close()
        fmt = logging.Formatter(format)    #フォーマッタの作成
        fh = logging.FileHandler(filename) #ファイルハンドラの生成
        fh.setFormatter(fmt)               #ファイルハンドラにフォーマッタを登録
        self.logger.addHandler(fh)         #ロガーにファイルハンドラを登録
        
        #標準出力の出力指示がされていたら、標準出力用のハンドラとフォーマッタを登録
        if stdout:
            sd = logging.StreamHandler()
            sd.setFormatter(fmt)     
            self.logger.addHandler(sd)

    def __setLevel(self,level_str):
        '''
        ログに出力するエラーレベルを設定する

        Parameters
        ----------
        level_str:str
            ログの出力レベル
            DEBUG=10  INFO=20 WARINNG=30 ERROR=40 CRITICAL=50
        '''
        level = 20
        if level_str == 'DEBUG':
            level = 10
        elif level_str == 'WARINNG':
            level = 30
        elif level_str == 'ERROR':
            level = 40
        elif level_str == 'CRITICAL':
            level = 50
        self.logger.setLevel(level)

    def __create_log_path(self):
        '''
        __file__ の内容を使って、ログファイルのパスの初期値を生成する
        '''
        today=datetime.date.today()
        folder = os.path.join(self.__get_parent(__file__),'logs')
        if os.path.exists(folder) == False:
            os.makedirs(folder)
        name_today_prefix = today.strftime('%Y%m%d')
        filename = os.path.join(folder,name_today_prefix+'.log')

        return filename
    
    def __get_parent(self,path):
        '''
        指定したパスの１つ上のフォルダ（親フォルダ）を返す

        Parameters
        ----------
        path:str
            ファイルパス
        '''
        return '\\'.join(os.path.dirname(path).split('\\')[0:-1])
    
    def __get_file_name_and_line_no_caller(self):
        '''
        呼び出し元ファイル名、行数を返す
        '''
        target_stack_trace = inspect.currentframe().f_back.f_back
        return target_stack_trace.f_code.co_filename+' '+str(target_stack_trace.f_lineno)+' '