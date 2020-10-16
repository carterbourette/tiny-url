from tinyurl.database import Database
import hashlib, base64

class URL:
    """URL - A container for URL parsing, hashing, and retrieval."""

    @staticmethod
    def hash(url):
        """hash - A space and time efficient hash function.
        
        Based on https://www.peterbe.com/plog/best-hashing-function-in-python
        """
        return base64.urlsafe_b64encode(
            hashlib.md5(url.encode()) \
            .digest()
        ).decode()[:6]


    @staticmethod
    def create(hash_id, url):
        return Database.execute('insert into url (hash, url) values (%s, %s)', 
            (hash_id, url))


    @staticmethod
    def find(hash_id):    
        return Database.query('select url, hash from url where hash = %s',
            (hash_id,), get_one=True)


    @staticmethod
    def minify(url):
        """minify - Take a url and create an associated tinyurl record.
        
        Create a new url entry using the created hash if the creation fails, 
        hash the collision, repeat until successfully created.
        """
        to_hash = url
        while True:
            url_hash = URL.hash(to_hash)
            if URL.create(url_hash, url):
                break
            
            to_hash = url_hash

        return { 'hash': url_hash, 'url': url }
