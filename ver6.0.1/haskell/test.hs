data Ml1 a = Mil
    | Ml a (Ml1 a)

(+-) :: a -> Ml1 a -> Ml1 a
(+-) a b = Ml a b

fn :: Ml1 Rational
fn = 1 +- ((fac 1000) +- Mil)


printL :: Show a => Ml1 a -> [Char]
printL (a `Ml` Mil) = show a
printL (Ml a s) = (show a) ++ (printL s)
printL Mil = ""

n0 = \ f x -> x
n1 = \ f x -> f x
succM = \ a f x -> f (a f x)
mult = \ a b f x -> a (b f) x

-- y::(tic->tic)->tic
y = \f -> f (y f)
fac = y (\fac x ->  if x <= 1 then 1 else x * fac (x-1))

main :: IO ()
main = putStrLn (show (
    fibN 1000000
    ))
manyA :: [Int]
manyA = let manyA = (\(a:b:_) -> a:(manyA (b:a+b:[]))) in
    manyA (1:1:[])

fibN::Int -> Int
fibN = (y (\fib a b n -> if n == 1 then a else fib b (a+b) (n-1))) 1 1

