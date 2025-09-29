rule Base64_Fernet_Encryption {
    strings:
        // Import statements
        $import1 = "from cryptography.fernet import Fernet"
        $import2 = "import base64"

        // Base64 operations
        $b64_1 = "base64.urlsafe_b64encode"
        $b64_2 = "base64.b64encode"

        // Fernet initialization and usage
        $fernet1 = "Fernet("
        $fernet2 = ".encrypt("

        // String encoding operations
        $encode1 = ".encode()"
        $encode2 = ".decode()"

    condition:
        // Require both imports
        all of ($import*) and
        // And at least one base64 operation
        1 of ($b64*) and
        // And Fernet usage
        all of ($fernet*) and
        // And string encoding
        1 of ($encode*)
}
