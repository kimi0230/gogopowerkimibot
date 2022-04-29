def acquireLock(conn, lockname, identifier, expire=10):
    if conn.setnx(lockname, identifier):
        conn.expire(lockname, expire)
        return True
    else:
        return False


if __name__ == "__main__":
    pass
