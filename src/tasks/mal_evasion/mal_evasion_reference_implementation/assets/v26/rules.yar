rule Password_Hasher_PBKDF2
{
    strings:
        // Cryptographic function names
        $crypto_func = "pbkdf2_hmac" ascii
        $hash_alg = "sha256" ascii

        // Imports and encoding
        $imp_base64 = "base64" ascii
        $imp_hashlib = "hashlib" ascii
        $imp_os = "import os" ascii

        // Base64 encode function calls
        $b64_encode = "b64encode" ascii

        // Random generation
        $urandom = "urandom" ascii

        // Common numeric values
        $salt_len = "32" ascii
        $iterations = "100000" ascii

    condition:
        // Must have core crypto function and algorithm
        $crypto_func and $hash_alg and

        // Must have required imports
        all of ($imp_*) and

        // Must have encoding function
        $b64_encode and

        // Must have random generation
        $urandom and

        // Should have typical parameter values
        ($salt_len or $iterations)
}
