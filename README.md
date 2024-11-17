# Research

##  Rules for candles

### definitions
#### ci
> (Candlestick). A candlestick c = (date, op, hp, lp, cp)
is a tuple consists of a date and four intra-day prices of a stock.
A candlestick c is a basic element in the identification of the
candlestick patterns. The date, op, hp, lp and cp, represent the
date, opening price, high price, low price and closing price at the
‘‘date’’ position in a time series. For the purpose of simplification,
we use ci to denote the ith candlestick (datei, opi, hpi, lpi, cpi).
#### T
>  (Candlestick Time Series). A candlestick time series
T = {c1, c2, . . . , cn} is a sequence of candlesticks of a stock and
consists of n candlesticks from day 1 to day n. For the purpose of
simplification, T [ci, cj] is used to denote a subsequence of T from
ci to cj.
#### S
> (Significant Candlesticks). S = {c1, c2, . . . , cn} is a
subsequence of T and includes n candlesticks.
#### TC
> (Trend Candlesticks). TC = {c1, c2, . . . , cn} is a subse-
quence of T and composed of n candlesticks. In this paper, we set
n = 8 for defining a Trend Candlesticks. TC is always followed by
S.
#### STC
>  (Sub-trend Candlesticks). STC = {c1, c2, . . . , cn} is a
subsequence of TC and includes n consecutive candlesticks. In this
paper, we set n = 5 for a defining a Sub-trend Candlesticks. For
the purpose of simplification, we use STC[ci, ci+5] to denote the
subsequence of TC from ci to ci+5.
#### CanP
> (Candlestick Pattern). CanP = {TC, S} is a subse-
quence of T that comprises of two parts: trend candlesticks and
significant candlesticks.

### functions
#### len
>len(T ) returns the number of basic candlesticks of an
input sequence. If T = {c1, c2, . . . , ci}, then
len(T ) = i. 
#### white body
>  white_body(ci) returns true when the opening price
of a candlestick ci is less than its closing price.
white_body(c1) ≡ op(ci) < cp(ci). 
#### op
>  op(ci) returns the opening price of a candlestick ci.
op(ci) = opi. 
#### cp
>  cp(ci) returns the closing price of a candlestick ci.
cp(ci) = cpi. 
#### hp
>  hp(ci) returns the high price of a candlestick ci.
hp(ci) = hpi.
#### lp
>  lp(ci) returns the low price of a candlestick ci.
lp(ci) = lpi. 
#### tp_body
> tp_body(ci) returns the top of the body of a candlestick
ci. The top is the maximum value between the opening price and the
closing price.
tp_body(ci) = max(op(ci), cp(ci)) 
#### bm_body
> bm_body(ci) returns the bottom of the body of a can-
dlestick ci. The bottom is the minimum value between the opening
price and the closing price.
bm_body(ci) = min(op(ci), cp(ci))
#### sli_less
> sli_less(x, y) returns true when x is slightly less than
y in the range from 0.3% to 1%, where the interval is left-closed and
right-open.
lar_less(x, y) ≡ 0.3% ≤ [(y − x)/x] < 1%
#### small_body
> small_body(ci) returns true when the size of candle-
stick ci is small.
small_body(ci) ≡ sli_less(bm_body(ci), tp_body(ci)). 
#### us
> us(ci) returns the height of the upper shadow of a
candlestick ci.
us(ci) = hp(ci) − tp_body(ci). 
#### ls
> ls(ci) returns the height of the lower shadow of a
candlestick ci.
ls(ci) = bm_body(ci) − lp(ci). 
#### hs
> hs(ci) returns the total height of the shadows of a
candlestick ci.
hs(ci) = us(ci) + ls(ci). 
#### hb
> hb(ci) returns the height of the body of a candlestick
ci.
hb(ci) = |cp(ci) − op(ci)|. 
#### ap
> ap(STC) returns the average closing price of STC.
ap(STC) = (cp5 + cp4 + cp3 + cp2 + cp1)/5. 
#### pt
>  pt(TC) returns 1 when the price trend of TC is upward
and return -1 when the price trend of TC is downward.
pt(TC) = {
1, ap(STC[c1, c5]) < ap(STC[c2, c6])
< ap(STC[c3, c7]) < ap(STC[c4, c8])
−1, ap(STC[c1, c5]) > ap(STC[c2, c6])
> ap(STC[c3, c7]) > ap(STC[c4, c8])



### patterns
#### hammer
> (len(S) = 1) ∧ (pt(TC) = −1) ∧ small_body(s1)∧
!no_ls(s1) ∧ (2 ∗ hb(s1) < ls(s1) < 3 ∗ hb(s1))
∧(small_us(s1) ∨ no_us(s1)).
#### Advance Block 

> (len(S) = 3) ∧ (pt(TC) = 1) ∧ (∃s1, s2, s3 ∈ S ⇒
white_body(s1) ∧ white_body(s2)∧
white_body(s3) ∧ (op(s1) < op(s2) < cp(s1))∧
(op(s2) < op(s3) < cp(s2))∧
(hs(s3) > hb(s3)) ∧ (hs(s2) > hb(s2))∧
(hs(s3) > hs(s1)) ∧ (hs(s2) > hs(s1))).