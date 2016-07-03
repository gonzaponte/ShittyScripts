"""
Copyright (c) 2012, 2013 The PyPedia Project, http://www.pypedia.com
<br>All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: 

# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

http://www.opensource.org/licenses/BSD-2-Clause
"""

__pypdoc__ = """
Method: Tupper_self_referential_formula
Link: http://www.pypedia.com/index.php/Tupper_self_referential_formula
Retrieve date: Mon, 08 Feb 2016 13:31:06 -0500



Plots the [http://en.wikipedia.org/wiki/Tupper's_self-referential_formula Tupper's_self-referential_formula]:
: <math>{1\over 2} < \left\lfloor \mathrm{mod}\left(\left\lfloor {y \over 17} \right\rfloor 2^{-17 \lfloor x \rfloor - \mathrm{mod}(\lfloor y\rfloor, 17)},2\right)\right\rfloor</math>

The plot is the very same formula that generates the plot. 

[[Category:Validated]]
[[Category:Algorithms]]
[[Category:Math]]
[[Category:Inequalities]]


"""

def Tupper_self_referential_formula():

	k = 4858450636189713423582095962494202044581400587983244549483093085061934704708809928450644769865524364849997247024915119110411605739177407856919754326571855442057210445735883681829823754139634338225199452191651284348332905131193199953502413758765239264874613394906870130562295813219481113685339535565290850023875092856892694555974281546386510730049106723058933586052544096664351265349363643957125565695936815184334857605266940161251266951421550539554519153785457525756590740540157929001765967965480064427829131488548259914721248506352686630476300

	def f(x,y):
		d = ((-17 * x) - (y % 17))
		e = reduce(lambda x,y: x*y, [2 for x in range(-d)]) if d else 1
		f = ((y / 17) / e)
		g = f % 2
		return 0.5 < g

	for y in range(k+16, k-1, -1):
		line = ""
		for x in range(0, 107):
			if f(x,y):
				line += "@"
			else:
				line += " "
		print line


#Method name =Tupper_self_referential_formula()
if __name__ == '__main__':
    print __pypdoc__

    returned = Tupper_self_referential_formula()
    if returned:
        print 'Method returned:'
        print str(returned)
