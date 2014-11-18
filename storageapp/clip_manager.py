# -*- coding: utf-8 -*-
from flask import send_file, jsonify, Response
import os.path
import sys

class ClipManager():
    DIR_CAPACITY = 10000

    def __init__(self, config):
        self.clips_path = config['CLIPS_PATH']
        
        if not os.path.exists(self.clips_path):
            os.makedirs(self.clips_path)

        self.eblob_instance = None

        if (config['EBLOB_STORAGE']):
            sys.path.append(config['LIBEBLOB_PATH'])
            from libeblob_python import eblob, eblob_config
                    
            eb_config = eblob_config()
            eb_config.file = os.path.join(self.clips_path, 'data')
            eb_config.blob_size = config['EBLOB_BLOB_SIZE']
            
            self.eblob_instance = eblob(os.path.join(self.clips_path, 'log_file.txt'), 0, eb_config)


    def get_clip(self, clip_meta): 
        if self.eblob_instance:
            return Response(self._eblob_reader(clip_meta), mimetype='video/' + clip_meta.container_format)
               
        mypaths = self._path_maker(clip_meta)
        
        if not os.path.isfile(mypaths['full_name']):
            return jsonify(error_message='no clip with id {0}'.format(clip_meta.id)), 404
        
        return send_file(mypaths['full_name'], mimetype='video/' + clip_meta.container_format)


    def write_clip(self, clip_meta, data):
        if self.eblob_instance:
            self._eblob_writer(clip_meta, data)
            return True
        
        mypaths = self._path_maker(clip_meta)

        if not os.path.exists(mypaths['directory']):
            os.makedirs(mypaths['directory'])

        try:
            data.save(mypaths['full_name'])
            return True
        except:
            return False


    def _path_maker(self, clip_meta):
        directory = os.path.join(self.clips_path,
            str(clip_meta.id // self.DIR_CAPACITY))
            
        file_name = str(clip_meta.id) + '.' + clip_meta.container_format
        return {
            'file_name': file_name,
            'directory': directory,
            'full_name': os.path.join(directory, file_name)
        }
        
        
    def _eblob_reader(self, clip_meta):
        return self.eblob_instance.read_hashed(str(clip_meta.id), 0, 0)
        
        
    def _eblob_writer(self, clip_meta, data):
        raw_data = data.read()
        self.eblob_instance.write_hashed(str(clip_meta.id), raw_data, 0, 0)
    
