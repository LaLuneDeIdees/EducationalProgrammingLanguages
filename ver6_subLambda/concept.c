word = [a-zA-Z0-9!@#$%^&*_+=-`~[]{}";/,|?<>:]+
char = \'.\'
string = '((\')|[^'])((\')|[^'])+'
number = (+|-)[0-9]
abs = \
point = .
infixFlag = infix | infixr
nln = \n
os = (
cs = )

===========================

Start = dec Start

dec = options word is expr \n*

options = infixFlag number | empty

expr = abs | var var* | ( exprInScobe )
exprInScobe = \n* absInScobe \n*  | \n* var \n*  (var \n*)*  | \n* ( exprInScobe ) \n*

abs = \ word word* . expr
absInScobe = \ word \n* (word \n*)* . exprInScobe

var = word | number | string | char

data List a is 
  Nil
  Cons -> a (List a)

-- castTo
type List a is r -> (a -> List a -> r) -> r

Nil as List a
Nil is \Nil List . Nil

Cons as a -> List a -> List a
List is \a b Nil List . List a b

caseList as List a -> r -> (a -> List a -> r) -> r
caseList is \a Nil Cons. a Nil Cons

infixr 1 : is
  Cons



I as Num -> Num
I is \x.x


type Num is r -> (Num -> r) -> r

0 as Num
0 is
  \x y.x

succ as Num -> Num
succ is
  \n x y.y n

pred as Num -> Num
pred is
  \n.n 0 I

caseNum as Num -> a -> (Num -> a) -> a
caseNum is \n Zero More.n Zero More

Y as (a -> Num) -> Num
Y is \f.w (\x.f (x x))

ff as (a -> b)->a->b
ff is \FacLin p.FacLin p

fff is \FacLin n.case n (1) (ff FacLin)
  typeof \FacLin n.case n (1) (ff FacLin) = (Num -> Num) -> Num -> Num
    type FacLin = Num -> Num
    type \n.case n 1 (ff FacLin) = Num -> Num
      type n = Num
      type case n 1 (ff FacLin) = Num
        type case n 1 = (Num -> Num) -> Num
          type 1 = Num
          type case n = Num -> (Num -> Num) -> Num
            type case = Num -> Num -> (Num -> Num) -> Num
            type n = Num
        type (ff FacLin) = a -> b
          type ff = (a -> b)->a->b
          type FacLin = Num -> Num
typeof fff is (Num -> Num) -> Num -> Num

FacLin as Num -> Num
FacLin is
  Y fff
  type Y fff = Num -> Num
  type Y = (a->a)->a
  type fff = (Num -> Num) -> Num -> Num




add as Num -> Num -> Num
add is
  Y \add a b. caseNum b
      a
      (\p1. caseNum a
          b
          (add (succ a) p1)



type List a is r -> (a -> List a -> r) -> r

Cons as a -> List a -> List a
Cons is 
  \a b Nil Cons.Cons a b

Nil as List a
Nil is
  \Nil Cons. Nil

type Bool is r -> r -> r
True as Bool
True is \x y.x
False as Bool
False is \x y.y



-- how i can do overloading
infix 7 + as a -> a -> a

instance + as Num -> Num -> Num
  is add

instance + as List a -> List a -> List a
  is Y \add l1 l2.l1 l2 (\d ds.add (ds) (Cons d l2))

-- algoritms for overloading
-- ...



data Expr a is
  N Num
  B Bool
  Add (Expr Num) (Expr Num)
  Eq (Expr Bool) (Expr Bool)

type Expr a is (Num -> r) -> (Bool -> r) -> (Expr Num -> Expr Num -> r) -> (Expr Bool -> Expr Bool -> r) -> r

N as Num -> Expr Num
B as Bool -> Expr Bool
Add as Expr Num -> Expr Num -> Expr Num
Eq as Expr Bool -> Expr Bool -> Expr Bool
caseExpr as (Expr a) -> (Num -> r) -> (Bool -> r) -> (Expr Num -> Expr Num -> r) -> (Expr Bool -> Expr Bool -> r) -> r


f1 = \eval a b.add (eval a) (eval b)
f2 = \eval a b.eq (eval a) (eval b)

eval as Expr a -> a
eval is
  Y \eval expr.(
    caseExpr expr
    -- Number
      I
    -- Boolean
      I
    -- Add
      f1 eval
    -- Equal
      f2 eval
  )


