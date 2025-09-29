rule Flask_JSON_Logger {
    meta:
        description = "Detects Flask application with JSON logging capabilities"

    strings:
        // Import statements
        $import1 = "from flask import Flask"
        $import2 = "import json"
        $import3 = "import logging"

        // Configuration strings
        $log_config = "logging.basicConfig"
        $log_file = "out.log"

        // Flask specific strings
        $flask_route = "@app.route('/',"
        $flask_post = "methods=['POST']"
        $template = "index.html"

        // JSON and logging functionality
        $json_get = "get_json()"
        $json_dumps = "json.dumps"
        $log_info = "logging.info"

        // Template rendering
        $render = "render_template"

    condition:
        // Must have at least 2 core Flask imports
        2 of ($import*) and

        // Must have logging configuration
        $log_config and $log_file and

        // Must have Flask route with POST method
        $flask_route and $flask_post and

        // Must have template rendering
        $template and $render and

        // Must have JSON handling
        $json_get and $json_dumps and

        // Must have logging call
        $log_info
}
