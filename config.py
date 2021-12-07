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

from supybot import conf, registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Pastebin2cpaste')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    Pastebin2cpaste = conf.registerPlugin('Pastebin2cpaste', True)
    curl = expect("""Curl Command (%s will be replaced by the URL):""",
                  [], default="""curl '%s'""")
    cpaste = expect("""Cpaste Command:""", [],
                    default="""rpaste -x 1day < /etc/os-release 2>/dev/null | sed -n -E 's/^Paste URL: +//p'""")
    Pastebin2cpaste.curl.setValue(curl)
    Pastebin2cpaste.cpaste.setValue(cpaste)

Pastebin2cpaste = conf.registerPlugin('Pastebin2cpaste')
# This is where your configuration variables (if any) should go.  For example:
conf.registerGlobalValue(Pastebin2cpaste, 'curl',
    registry.String("""curl '%s'""", _("""Curl Command (%s will be replaced bu the URL).""")))
conf.registerGlobalValue(Pastebin2cpaste, 'cpaste',
    registry.String(
        """cpaste -a "CentOS Project Repaste Service" -p -s -e 1440""",
        _("""Cpaste Command.""")))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
