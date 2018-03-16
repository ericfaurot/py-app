#
# Copyright (c) 2018 Eric Faurot <eric@faurot.net>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
import logging
import logging.handlers

_logger = None

def init(config, foreground = False):
    global _logger

    procname = config['procname']
    logfile = config['logfile']
    backupCount = config.getint('log.maxfile', 10)
    maxBytes = config.getint('log.maxsize', 10 * 1024 * 1024)

    logname = procname

    if foreground:
        # Log to stderr.
        logging.basicConfig(level = "DEBUG")
        logger = logging.getLogger(logname)

    else:
        formatter = logging.Formatter(fmt = " ".join(["%(asctime)s",
                                                      "%s[%%(process)s]:" % procname,
                                                      "%(levelname)s:",
                                                      "%(message)s" ]),
                                      datefmt = "%Y-%m-%d %H:%M:%S")
        handler = logging.handlers.RotatingFileHandler(logfile,
                                                       maxBytes = maxBytes,
                                                       backupCount = backupCount)
        handler.setLevel("INFO")
        handler.setFormatter(formatter)
        logger = logging.getLogger(logname)
        logger.addHandler(handler)
        logger.setLevel("INFO")

    _logger = logger

    return logger

def info(*args):
    _logger.info(*args)

def warn(*args):
    _logger.warn(*args)

def error(*args):
    _logger.error(*args)
