import os
import unittest
import storageapp.app
from storageapp.app import app, init_app
from storageapp.database import init_db
from storageapp.clip_manager import ClipManager
import json
import sys
from tempfile import gettempdir
from datetime import datetime
from shutil import rmtree


class UserapiAppTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = os.path.join(gettempdir(), 
            datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        os.makedirs(self.tempdir)
        
        app.config['CLIPS_PATH'] = self.tempdir
        app.config.from_object('tests.test_settings')
        app.config['EBLOB_STORAGE'] = False
        
        init_app()
        self.app = app.test_client()
        init_db()
        
        self.stream_id = 0
        self.clip_id = 1


    def tearDown(self):
        print self.tempdir
        rmtree(self.tempdir)


    def test_hello(self):
        rv = self.app.get('/hello')
        print rv.data
        assert rv.data


    def test_get_meta(self):
        self.stream_id += 1
        start_time = 1000
        rv = self.app.get('/teststorage/add/{0}/{1}'.format(self.stream_id, start_time))
        
        assert rv.status_code == 200
        
        rv = self.app.get('/get_meta?stream_id={0}&start_time={1}&stop_time={2}'\
            .format(self.stream_id, start_time, start_time + 100))
            
        assert rv.status_code == 200
        
        janswer = json.loads(rv.data)
        print janswer
        assert janswer['clips']


    def test_file_mode(self):        
        self.clip_add_then_get_method()

    
    def test_eblob_mode(self):
        app.config['EBLOB_STORAGE'] = True
        
        storageapp.app.clip_manager = ClipManager(app.config)
        
        self.clip_add_then_get_method()


    def clip_add_then_get_method(self):
        self.stream_id += 1
        rv = self.app.post('/add_clip',
            content_type = 'multipart/form-data',
            data = {
                'stream_id' : self.stream_id, 
                'start_time' : 1000,
                'stop_time' : 1200,
                'container_format' : 'mp4',
                'data' : ( 'tests/2.mp4', 'tests/2.mp4' )})
                
        print rv.data
        assert rv.status_code == 200
        
        self.clip_id = (json.loads(rv.data))['clip_id']
        rv = self.app.get('/get_clip/{0}'.format(self.clip_id))
        
        assert rv.data
        assert rv.status_code == 200


if __name__ == '__main__':
    unittest.main()
