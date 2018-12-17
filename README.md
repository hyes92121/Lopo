
## Resourses
All US-Stocks & ETFs from 2005 to 2017:
https://www.dropbox.com/s/9zpwaffnx0oy1hb/US-Stocks%26ETF-2005-2017.zip?dl=0

Stock sectors:
https://money.usnews.com/investing/stocks/rankings

Pomegranate-Hidden Markov Model:
https://pomegranate.readthedocs.io/en/latest/HiddenMarkovModel.html


## Stock sectors 
Industrial Machinery: gtls,grc,dxpe,fls,evi,iex<br />
Airlines: skyw,ual,dal,luv,ryaay,cpa,aal<br />
Major banks: pebo,wf,fbms,jpm,bbt,ry,bmo,usb,bk,cm,pnc,cof,bac<br />
Oil & Gas Production: pnrg,cop,wll,ceo,hes,isrl,eog,mur<br />
Electronic Components: vicr,cree,cts,glw,aph,vsh,plxs,jbl,sanm<br /> 
Semiconductors:amd,idti,mlnx,smtc,xlnx,intc,diod,adi<br />

Experiments:
pnrg,cop,ceo,hes,mur,isrl -> ceo

## Usage
```bash
python hmm.py -c <stockcode_list> -d <date_range> -t <stock_to_be_modeled>
```

Example:
```bash
python hmm.py -c pnrg,cop,ceo,hes,mur,isrl -d 2011-03-01,2017-03-01 -t isrl
```
