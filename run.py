#!/usr/bin/env python

#po/Speak is licensed under the GPL v3.0 <gpl-3.0.txt>
#(c)2015-present Kamil Mansuri <twitter: @supermansuri>

#Flask is licensed under the BSD license
#gunicorn is licensed under the MIT license
#tinyurl algorithm is based on the work of Michael Fogleman and is licensed under the MIT license

from pospeakapp import app

if __name__ == "__main__":

    #app.run(debug=True)
    app.run()