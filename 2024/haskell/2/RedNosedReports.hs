import Data.Ix (inRange, Ix)

-- Function to read and parse the input file into two arrays of numbers
parseInput :: FilePath -> IO [[Int]]
parseInput filename = do
    content <- readFile filename
    let linesOfFile = lines content
    let numbers = map (map read . words) linesOfFile
    return numbers


-- Function to read input
readInput :: IO [[Int]]
readInput = parseInput "input.txt"


ascending :: (Ord a) => [a] -> Bool
ascending [] = True
ascending [x] = True
ascending (x:y:xs) = x < y && ascending (y:xs)

descending :: (Ord a) => [a] -> Bool
descending [] = True
descending [x] = True
descending (x:y:xs) = x > y && descending (y:xs)

monotonic :: (Ord a) => [a] -> Bool
monotonic xs = ascending xs || descending xs


inStep :: (Num a, Ix a) => [a] -> Bool
inStep [] = True
inStep [x] = True
inStep (x:y:xs) = inRange (1, 3) (abs (x-y)) && inStep (y:xs)

isSafe :: (Num a, Ix a, Ord a) => [a] -> Bool
isSafe xs = inStep xs && monotonic xs

countTrue = length . filter id


partOne :: IO ()
partOne = do
    input <- readInput
    let safe = map isSafe input
    let totalSafe = countTrue safe
    print totalSafe


lenientCheck :: (a -> a -> Bool) -> [a] -> Bool
lenientCheck pred xs = 
    checkAdjacent pred xs || 
    case findFirstFailure pred xs of
        Nothing -> True
        Just i  -> checkAdjacent pred (removeAt xs i) ||
                   checkAdjacent pred (removeAt xs (i+1))

checkAdjacent :: (a -> a -> Bool) -> [a] -> Bool
checkAdjacent pred xs = and $ zipWith pred xs (tail xs)

findFirstFailure :: (a -> a -> Bool) -> [a] -> Maybe Int
findFirstFailure pred xs = 
    findIndex not $ zipWith pred xs (tail xs)


partTwo :: IO ()
partTwo = do
    input <- readInput
    print input


main :: IO ()
main = do
    partOne
    -- partTwo