from django.contrib.auth.hashers import BCryptPasswordHasher

class CustomBCryptPasswordHasher(BCryptPasswordHasher):
    """
    Custom password hasher that removes the 'bcrypt$$' prefix from hashes.
    """
    algorithm = "bcrypt"

    def encode(self, password, salt):  # sourcery skip: avoid-builtin-shadow
        # Use the parent class to generate the hash
        hash = super().encode(password, salt)
        # Remove the 'bcrypt$$' prefix
        return hash.replace("bcrypt$", "")