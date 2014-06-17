#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import xapian_indexer

from fuse import FUSE, FuseOSError, Operations


class myFS(Operations):
    def __init__(self, root):
        self.root = root

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        print 'Invoking access'
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        print 'Invoking chmod'
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        print 'Invoking chown'
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        print 'Invoking getattr'
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        print 'Invoking readdir'
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        print 'Invoking readlink'
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        print 'Invoking mknod'
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        print 'Invoking rmdir'
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        print 'Invoking mkdir'
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        print 'Invoking statfs'
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        print 'Invoking unlink'
        return os.unlink(self._full_path(path))

    def symlink(self, target, name):
        print 'Invoking symlink'
        return os.symlink(self._full_path(target), self._full_path(name))

    def rename(self, old, new):
        print 'Invoking rename'
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        print 'Invoking link'
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        print 'Invoking utimens'
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        print 'Invoking open'
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        print 'Invoking create'
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        print 'Invoking read'
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        print 'Invoking write'
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        print 'Invoking truncate'
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        print 'Invoking flush ', path
        return os.fsync(fh)

    def release(self, path, fh):
        print 'Invoking release ', path
        print "I'm goind to index/re-index document at this path: ", path

        xapian_indexer.index({
                'filename': path.split('/')[-1],
                'filepath': path,
                'description': '',
                'tags': '',
                'content': ''
            })
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        print 'Invoking fsync'
        return self.flush(path, fh)


def main(root, mountpoint):
    FUSE(myFS(root), mountpoint, foreground=True)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
