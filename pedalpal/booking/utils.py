from django.utils import timezone
from booking.models import Booking
import base64, re
from Crypto.Cipher import AES
from Crypto import Random
import os


def end_expired_bookings():
    now = timezone.now()
    bookings = Booking.objects.filter(end_time=None)

    for booking in bookings:
        if booking.start_time < now:
            booking.end_time = now
            booking.save()
            booking.cycle.booked = False
            booking.cycle.user = None
            booking.cycle.active = False
            booking.cycle.save()

            print(f"Booking {booking.id} ended.")
        else:
            print(f"Booking {booking.id} not ended.")


class AESCipher:
    """
    Usage:
    aes = AESCipher( settings.SECRET_KEY[:16], 32)
    encryp_msg = aes.encrypt( 'ppppppppppppppppppppppppppppppppppppppppppppppppppppppp' )
    msg = aes.decrypt( encryp_msg )
    print("'{}'".format(msg))
    """

    def __init__(self, blk_sz):
        self.key = os.getenv("SECRET_KEY")[:16]
        self.blk_sz = blk_sz

    def encrypt(self, raw):
        if raw is None or len(raw) == 0:
            raise NameError("No value given to encrypt")
        raw = raw + "\0" * (self.blk_sz - len(raw) % self.blk_sz)
        raw = raw.encode("utf-8")
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key.encode("utf-8"), AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode("utf-8")

    def decrypt(self, enc):
        if enc is None or len(enc) == 0:
            raise NameError("No value given to decrypt")
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key.encode("utf-8"), AES.MODE_CBC, iv)
        return re.sub(b"\x00*$", b"", cipher.decrypt(enc[16:])).decode("utf-8")
