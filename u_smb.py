# -*- coding:utf-8 -*-
# @Author: wzy
# @Time: 2021/3/18
# SMB协议下的共享盘文件操作, 依赖于第三方包 pysmb !!
__all__ = ["SMBClient"]

import io
import os

# 依赖于第三方包 pysmb
from smb.SMBConnection import SMBConnection, OperationFailure


class SMBClient:
    """
    SMB连接客户端
    """
    status = False
    samba = None

    def __init__(self, username: str, password: str, ip: str, port: int = 139):
        self.username = username
        self.password = password
        self.ip = ip
        self.port = port
        self.samba = SMBConnection(self.username, self.password, '', '', use_ntlm_v2=True)
        self.samba.connect(self.ip, self.port)
        self.status = self.samba.auth_result

    def close(self):
        if self.status:
            self.samba.close()

    def list_smb_dir(self, share_name, sub_dir=""):
        """列出文件夹内所有文件名
        :param share_name:  共享文件夹名称
        :param sub_dir:     相对共享文件夹的子目录
        """
        file_names = list()
        for e in self.samba.listPath(share_name, sub_dir):
            if e.filename[0] != '.':  # 过滤上级文件夹及影藏文件
                file_names.append(e.filename)
        return file_names

    def download(self, filename, local_dir, share_name, sub_dir=""):
        """下载文件
        :param filename:    文件名
        :param share_name:  共享文件夹名称
        :param sub_dir:     相对共享文件夹的子目录
        :param local_dir:   本地保存文件夹路径
        """
        assert isinstance(filename, str)
        with open(os.path.join(local_dir, filename), 'wb') as fp:
            self.samba.retrieveFile(share_name, os.path.join(sub_dir, filename), fp)

    def download_bytes(self, share_name, sub_file_path):
        """直接下载共享文件的Bytes数据
        :param share_name:      共享文件夹名称
        :param sub_file_path:   共享文件路径
        """

        fp = io.BytesIO()
        self.samba.retrieveFile(share_name, sub_file_path, fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        return data

    def upload(self, local_file_path, share_name, smb_save_path):
        """上传文件
        :param local_file_path:     本地文件路径
        :param share_name:          共享文件夹名称
        :param smb_save_path:       在共享文件夹的存放路径
        """
        with open(local_file_path, "rb") as fp:
            self.samba.storeFile(share_name, smb_save_path, fp)

    def upload_bytes(self, data, share_name, smb_save_path):
        """直接将Bytes类型的数据保存到共享文件
        :param data:            Bytes类型数据
        :param share_name:      共享文件夹名称
        :param smb_save_path:   在共享文件夹的存放路径
        """
        fp = io.BytesIO(data)
        self.samba.storeFile(share_name, smb_save_path, fp)
        fp.close()

    def create_dir(self, share_name, sub_dir):
        """创建文件夹
        :param share_name:      共享文件夹名称
        :param sub_dir:         相对共享文件夹的子目录
        """
        self.samba.createDirectory(share_name, sub_dir)

    def file_attrs(self, share_name, smb_file_path):
        attrs = {}
        try:
            file = self.samba.getAttributes(share_name, smb_file_path)
            for attr in ['alloc_size', 'create_time', 'file_attributes', 'file_id', 'file_size', 'filename',
                         'isDirectory', 'isNormal', 'isReadOnly', 'last_access_time', 'last_attr_change_time',
                         'last_write_time', 'short_name']:
                attrs[attr] = getattr(file, attr)
        except OperationFailure:
            pass
        return attrs

    def delete_file(self, share_name, smb_file_pattern):
        """删除文件, 默认都把传入的smb_file_pattern转换为Unicode字符串
        :param share_name:          共享文件夹名称
        :param smb_file_pattern:    文件的相对路径, 可以使用通配符
        """
        self.samba.deleteFiles(share_name, smb_file_pattern)
