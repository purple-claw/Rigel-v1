import bencodepy
import hashlib

class TorrentManager:
    def __init__(self, torrent_file):
        self.torrent_file = torrent_file
        self.metadata = self.load_torrent()

    def load_torrent(self):
        try:
            with open(self.torrent_file, "rb") as f:
                return bencodepy.decode(f.read())
        except Exception as e:
            print(f"Error loading torrent file: {e}")
            return None

    def get_tracker_url(self):
        return self.metadata.get(b'announce', b'').decode()

    def get_info(self):
        return self.metadata.get(b'info', {})

    def get_torrent_name(self):
        info = self.get_info()
        return info.get(b'name', b'').decode()

    def get_total_size(self):
        info = self.get_info()
        if b'length' in info:
            return info[b'length']  # Single file
        elif b'files' in info:
            return sum(file[b'length'] for file in info[b'files'])  # Multiple files
        return 0

    def get_piece_length(self):
        """Returns the piece length in bytes."""
        info = self.get_info()
        return info.get(b'piece length', 0)

    def get_piece_count(self):
        info = self.get_info()
        pieces = info.get(b'pieces', b'')
        return len(pieces) // 20  # Each piece hash is 20 bytes

    def get_info_hash(self):
        info = self.get_info()
        encoded_info = bencodepy.encode(info)
        return hashlib.sha1(encoded_info).hexdigest()

if __name__ == "__main__":
    torrent = TorrentManager("puppy.torrent")
    print("Torrent Name:", torrent.get_torrent_name())
    print("Total Size:", torrent.get_total_size(), "bytes")
    print("Piece Length:", torrent.get_piece_length(), "bytes")
    print("Number of Pieces:", torrent.get_piece_count())
    print("Tracker URL:", torrent.get_tracker_url())
    print("Info Hash:", torrent.get_info_hash())
