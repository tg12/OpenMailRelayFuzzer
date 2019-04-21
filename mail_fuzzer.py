# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
# NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
# DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
# WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import random
import threading
from essential_generators import DocumentGenerator
import socket
import smtplib
from smtplib import *

port = 25
thread_list = []


def thread_worker(thread_no, me, you, svr):
    print("[+]trying...")
    # me == the sender's email address
    print("[+]from...\t\t" + str(me))
    # you == the recsvrient's email address
    print("[+]to...\t\t" + str(you))
    print("[+]server...\t\t" + str(svr))

    s = socket.socket()
    s.connect((svr, int(port)))
    socket.setdefaulttimeout(3)
    ans = s.recv(1024)

    if ("220" in ans):
        print(
            "\n[+]port" +
            " " +
            str(port) +
            " " +
            "open on the target system\n")
        smtpserver = smtplib.SMTP(svr, int(port))
        r = smtpserver.docmd("Mail From:", me)
        a = str(r)
        if ("250" in a):
            r = smtpserver.docmd("RCPT TO:", you)
            a = str(r)
            if ("250" in a):
                print(
                    "[+]The target system seems vulnerable to Open relay attack, FOUND!!\t\t" +
                    str(svr))
            else:
                print("[-]The target system is not vulnerable to Open relay attack ")
    else:
        print("[-]port is closed/Filtered")


while True:
    for thread_no in range(1):
        try:
            gen = DocumentGenerator()
            me = str(gen.email())
            you = str(gen.email())
            svr = ".".join(map(str, (random.randint(0, 255)
                                     for _ in range(4))))

            thread = threading.Thread(
                target=thread_worker, args=(
                    thread_no, me, you, svr))
            thread_list.append(thread)
            thread.start()

        except Exception as e:
            print(e)
            pass
