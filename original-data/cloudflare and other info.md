 workers code  

cexport default { 
  async fetch(request, env, ctx) {
    let { pathname, search, host } = new URL(request.url);
   
    // Remove /metrics/ prefix and replace with root path
    pathname = pathname.replace('/metrics/', '/');
   
    // Your sGTM domain
    const domain = 'sgtm.messerattach.com';
   
    // Create new request
    let newRequest = new Request((`https://` + domain + pathname + search), request);
    newRequest.headers.set('Host', domain);
   
    return fetch(newRequest);
  },
};


Order
Name
Match against
Action
Active
Menu

1
sGTM same origin Configuration

URI Path starts with /metrics

SSL


Origin Rules


0 active
Create rule
No Origin Rules created


Request Header Transform Rules

1/25 used
Create rule
Go to Managed Transforms
Order
Name
Match against
Action
Active
Menu

1
sGTM same origin Request Header Transform Rule

URI Path starts with /metrics

X-From-Cdn = cf-stape


Cache Rules

1/25 used
Create rule
Order
Name
Match against
Action
Active
Menu

1
sGTM - Bypass Cache

URI Path starts with /metrics

Bypass cache



		
Type

Name

Content

Proxy status

TTL

Actions

A
ftp
156.67.70.197

DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

A
messerattach.com
82.180.139.184

Proxied

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

A
staging
82.180.139.184

Proxied

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

AAAA
messerattach.com
2a02:4780:b:1107:0:845:4b41:4

Proxied

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA

messerattach.com
0 issue pki.goog
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA
messerattach.com
0 issue sectigo.com
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA
messerattach.com
0 issue letsencrypt.org
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA
messerattach.com
0 issuewild digicert.com
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA
messerattach.com
0 issue globalsign.com
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA
messerattach.com
0 issuewild letsencrypt.org
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA
messerattach.com
0 issuewild globalsign.com
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA
messerattach.com
0 issuewild comodoca.com
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA
messerattach.com
0 issuewild sectigo.com
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA
messerattach.com
0 issue digicert.com
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA
messerattach.com
0 issue comodoca.com
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME
466ae868fdb6d01cb6ff1291a7b1769b
verify.bing.com

DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME
autodiscover
autodiscover.outlook.com

DNS only

1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME
k2._domainkey
dkim2.mcsv.net
DNS only

1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME
k3._domainkey
dkim3.mcsv.net
DNS only

1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME
selector1._domainkey
selector1-messerattach-com._domainkey.messerattach.k-v1.dkim.mail.microsoft

DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME
selector2._domainkey
selector2-messerattach-com._domainkey.messerattach.k-v1.dkim.mail.microsoft

DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME
sgtm
us.stape.io

DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME
www
messerattach.com

Proxied

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

MX
messerattach.com
messerattach-com.mail.protection.outlook.com
0
DNS only

1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

TXT
_dmarc
"v=DMARC1; p=quarantine; sp=quarantine; rua=mailto:jana@messerattach.com"
DNS only

1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

TXT
messerattach.com
"v=spf1 include:spf.protection.outlook.com include:servers.mcsv.net include:_spf.google.com include:stapeio._spf -all"
DNS only

1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

TXT
messerattach.com
"pinterest-site-verification=7b3796714628a56e1eea8af6dbdf7e4a"
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.



TXT
messerattach.com
google-site-verification=fiz731cXh13n2i6MxpA2fsWkIEaXolT3PCbukunsESU
DNS only

1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.



TXT
messerattach.com
facebook-domain-verification=txeas96x5czqugihptijqbwut4uc0d
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.



TXT
messerattach.com
google-site-verification=QyLO0YrH6oTJITWi6CrFw5TlGGzksFGTXi4lK134CrM
DNS only

1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.



TXT
staging
google-site-verification=fTTtSpFpFTCpDG39XM-1h2xQcirsvlhaZhtMJXsoGwk
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.



TXT
titan2._domainkey
v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCegkHNnWiyi1X2CJwwU7huEp6ioiCSCex1QiwLVomDPwrdPjdEmdlYjfr0OrQTM3sv7VcMj9f84W7KLeD8eFITsbSDS9pj/ghPZrrqqZk/C2yf8x+Y3ey2bOQVHhD06PGZFixAgRnd84/9IkdfgZfDUzh+NmSgJG4spIA9ALowKwIDAQAB
DNS only

Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.
Type

Name

Content

Proxy status

TTL

Actions

A

ftp
156.67.70.197

DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

A

messerattach.com
82.180.139.184

Proxied
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

A

staging
82.180.139.184

Proxied
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

AAAA

messerattach.com
2a02:4780:b:1107:0:845:4b41:4

Proxied
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA

messerattach.com
0 issue pki.goog
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA

messerattach.com
0 issue sectigo.com
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA

messerattach.com
0 issue letsencrypt.org
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA

messerattach.com
0 issuewild digicert.com
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA

messerattach.com
0 issue globalsign.com
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA

messerattach.com
0 issuewild letsencrypt.org
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA

messerattach.com
0 issuewild globalsign.com
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA

messerattach.com
0 issuewild comodoca.com
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA

messerattach.com
0 issuewild sectigo.com
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA

messerattach.com
0 issue digicert.com
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CAA

messerattach.com
0 issue comodoca.com
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME

466ae868fdb6d01cb6ff1291a7b1769b
verify.bing.com

DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME

autodiscover
autodiscover.outlook.com

DNS only
1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME

k2._domainkey
dkim2.mcsv.net
DNS only
1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME

k3._domainkey
dkim3.mcsv.net
DNS only
1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME

selector1._domainkey
selector1-messerattach-com._domainkey.messerattach.k-v1.dkim.mail.microsoft

DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME

selector2._domainkey
selector2-messerattach-com._domainkey.messerattach.k-v1.dkim.mail.microsoft

DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME

sgtm
us.stape.io

DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

CNAME

www
messerattach.com

Proxied
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

MX

messerattach.com
messerattach-com.mail.protection.outlook.com
0
DNS only
1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

TXT

_dmarc
"v=DMARC1; p=quarantine; sp=quarantine; rua=mailto:jana@messerattach.com"
DNS only
1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

TXT

messerattach.com
"v=spf1 include:spf.protection.outlook.com include:servers.mcsv.net include:_spf.google.com include:stapeio._spf -all"
DNS only
1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.

TXT

messerattach.com
"pinterest-site-verification=7b3796714628a56e1eea8af6dbdf7e4a"
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.


TXT

messerattach.com
google-site-verification=fiz731cXh13n2i6MxpA2fsWkIEaXolT3PCbukunsESU
DNS only
1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.


TXT

messerattach.com
facebook-domain-verification=txeas96x5czqugihptijqbwut4uc0d
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.


TXT

messerattach.com
google-site-verification=QyLO0YrH6oTJITWi6CrFw5TlGGzksFGTXi4lK134CrM
DNS only
1 hr
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.


TXT

staging
google-site-verification=fTTtSpFpFTCpDG39XM-1h2xQcirsvlhaZhtMJXsoGwk
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.


TXT

titan2._domainkey
v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCegkHNnWiyi1X2CJwwU7huEp6ioiCSCex1QiwLVomDPwrdPjdEmdlYjfr0OrQTM3sv7VcMj9f84W7KLeD8eFITsbSDS9pj/ghPZrrqqZk/C2yf8x+Y3ey2bOQVHhD06PGZFixAgRnd84/9IkdfgZfDUzh+NmSgJG4spIA9ALowKwIDAQAB
DNS only
Auto
EditWhen toggled open, an additional table row will be added below this row to enable editing DNS records.