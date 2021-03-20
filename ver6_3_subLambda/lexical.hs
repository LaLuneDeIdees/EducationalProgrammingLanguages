data RoseTree a b = Leaf a | Node b [RoseTree a b] 
data ParserState a = Err | Next (RoseTree a [Char]) [a]

empty::ParserState a -> ParserState a
empty s = s

term :: (Foldable t, Eq a) => Bool -> t a -> ParserState a -> ParserState a
term _ _ (Next _ []) = Err
term l a (Next (Node b c) (p1:ps))
    | l == True && (p1 `elem` a) = Next (Node b (c++[Leaf p1])) ps
    | l /= True && not (p1 `elem` a) = Next (Node b (c++[Leaf p1])) ps
    | otherwise = Err
term _ _ otherwise = Err


nterm :: [Char] -> (ParserState a -> ParserState a) -> ParserState a -> ParserState a
nterm n a p = case p of
    Next (Node nm1 ls1) p1 -> case a (Next (Node n []) p1) of
        Next dr p2 -> Next (Node nm1 (ls1 ++ [dr])) p2
        otherwise -> Err
    otherwise -> Err

nsterm :: (ParserState a -> ParserState a) -> ParserState a -> ParserState a
nsterm _ Err = Err
nsterm a p = case a p of
    Next dr p1 -> case p of
        Next dr0 p0 -> Next dr0 p1
        otherwise -> Err
    otherwise -> Err

tin:: Eq a =>  [a] -> ParserState a -> ParserState a
tin = term True
ton:: Eq a =>  [a] -> ParserState a -> ParserState a
ton = term False

rep::(ParserState a -> ParserState a) -> ParserState a -> ParserState a
rep _ Err = Err
rep f p = case (f p) of
    Err -> p
    Next d ps -> rep f (Next d ps)

ser::(ParserState a -> ParserState a) -> (ParserState a -> ParserState a) -> ParserState a -> ParserState a
ser _ _ Err = Err
ser a b p = case a p of
                Err -> Err
                p' -> b p'

(+/) :: (ParserState a -> ParserState a) -> (ParserState a -> ParserState a) -> ParserState a -> ParserState a
a +/ b = ser a b

oom :: (ParserState a -> ParserState a) -> ParserState a -> ParserState a
oom a = a +/ (rep a)

oon :: (ParserState a -> ParserState a) -> ParserState a -> ParserState a
oon _ Err = Err
oon a p = case a p of
    Err -> p
    p1 -> p1

par::(ParserState a -> ParserState a) -> (ParserState a -> ParserState a) -> ParserState a -> ParserState a
par _ _ Err = Err
par a b p = case a p of
    Err -> b p
    p1 -> p1

(|/) :: (ParserState a -> ParserState a) -> (ParserState a -> ParserState a) -> ParserState a -> ParserState a
a |/ b = par a b

word :: Eq a => [a] -> ParserState a -> ParserState a
word s = foldr1 (\x a -> ser x a) (map (\x -> tin [x]) s)

showTree :: (Show a1, Show a2) => RoseTree a1 a2 -> [Char]
showTree (Leaf a) = show a
showTree (Node n ls) = (show n) ++ "(" ++ (
    foldl (
        \a x->a ++ (showTree x) ++ ", "
        ) "" ls
    ) ++ ")"

wordt :: ParserState Char -> ParserState Char
wordt = nterm "WORD" $ oom $ tin "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321`~|]}[{+=_-*&^%$#@!';:/?.>,<"

number :: ParserState Char -> ParserState Char
number = nterm "Number" $ oom $ tin "0987654321"

space :: ParserState Char -> ParserState Char
space = nsterm.rep $ tin "\n\t \r"

subExpr :: ParserState Char -> ParserState Char
subExpr = (nsterm $ tin "(") +/ expr +/ (nsterm $ tin ")")

expr :: ParserState Char -> ParserState Char
expr = nterm "EXPR" $ space +/ rep ((number |/wordt|/ subExpr) +/ space)


data Expr = Expr [Expr] | Numb Double | Wordb [Char]

evalExpr :: Expr -> Maybe Double
evalExpr (Expr (w:a1:a2:[])) = case w of
    Wordb w -> do
        _a1 <- evalExpr a1
        _a2 <- evalExpr a2
        case w of
            "+" -> Just (_a1 + _a2)
            "-" -> Just (_a1 - _a2)
            "*" -> Just (_a1 * _a2)
            "/" -> Just (_a1 / _a2)
            otherwise -> Nothing
    otherwise -> Nothing
evalExpr (Numb a) = Just a
evalExpr (Wordb _) = Nothing
evalExpr _ = Nothing


convertToExpr :: RoseTree Char [Char] -> Maybe Expr
convertToExpr (Node "Number" w) = Just $ Numb (read (map (\x -> case x of
    Leaf a -> a
    otherwise -> ' ') w)::Double)
convertToExpr (Node "WORD" w) = Just $ Wordb (map (\x -> case x of
    Leaf a -> a
    otherwise -> ' ') w)
convertToExpr (Node "EXPR" w) = do
    ls <- mapM convertToExpr w
    Just $ Expr ls
convertToExpr otherwise = Nothing

main :: IO ()
main = do
    let b = expr (Next (Node "Root" []) "* (* (/ 3 7) (* 13 5)) (/ (/ 3 2) (/ 4 5))")
        a2 = do
            evale <- case b of 
                Next (Node _ (x:_)) _ -> convertToExpr x
                otherwise -> Nothing
            evalExpr evale
        a3 = case a2 of
            Nothing -> "error"
            Just a -> show a

    print a3