###
# Copyright (c) 2019, Peter Ajamian
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

from supybot import utils, plugins, ircutils, callbacks, ircmsgs
from supybot.commands import *
import subprocess
import re
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Pastebin2cpaste')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class Pastebin2cpaste(callbacks.Plugin):
    """Copies pastebin.com pastes to paste.centos.org using the cpaste command."""
    threaded = True

    # Data for various source pastebins.  The key must be the lowercase domain
    # name.  The regex must be compiled and should return the pastebin code as
    # the first match.  The url will have the pastebin code substituted for %s.
    pastebins = {
        'pastebin.com': {
            'regex': re.compile(r'([0-9a-zA-Z]+)[.:?!,]*$'),
            'url': 'https://pastebin.com/raw/%s'
        },
        'hastebin.com': {
            'regex': re.compile(r'/([a-z]+)(?:\.[a-z]+)?[.:?!,]*$'),
            'url': 'https://hastebin.com/raw/%s'
        },
        'www.irccloud.com': {
            'regex': re.compile(r'/pastebin(?:/raw)?/([0-9a-zA-Z]+)(?:/.*)?[.:?!,]*$'),
            'url': 'https://www.irccloud.com/pastebin/raw/%s'
        },
        'termbin.com': {
            'regex': re.compile(r'([0-9a-zA-Z]+)[.:?!,]*$'),
            'url': 'https://termbin.com/%s'
        },
        'paste.debian.net': {
            'regex': re.compile(r'([0-9]+)/?[.:?!,]*$'),
            'url': 'https://paste.debian.net/plain/%s'
        }
    }


    def doPrivmsg(self, irc, msg):
        if ircmsgs.isCtcp(msg) and not ircmsgs.isAction(msg):
            return
        channel = msg.args[0]
        if irc.isChannel(channel):
            if ircmsgs.isAction(msg):
                text = ircmsgs.unAction(msg)
            else:
                text = msg.args[1]
            for url in utils.web.httpUrlRe.findall(text):
                if not utils.web.getDomain(url).lower() in self.pastebins:
                    continue
                pastebin = self.pastebins[utils.web.getDomain(url).lower()]
                if pastebin:
                    pbCode = pastebin['regex'].search(url).group(1)
                    newURL = pastebin['url'] % pbCode
                    cmd = self.registryValue("curl") % newURL
                    cmd += "|" + self.registryValue("cpaste")
                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, shell=True)
                    o, e = proc.communicate()
                    if proc.returncode == 0:
                        irc.reply("Paste has been copied to "
                                  + o.decode('ascii').strip())

Class = Pastebin2cpaste


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
