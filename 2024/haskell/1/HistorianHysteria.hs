import System.IO
import Data.List
import Data.Map (Map, findWithDefault)
import qualified Data.Map as Map    

merge :: Ord a => [a] -> [a] -> [a]
merge a b
    | null a = b
    | null b = a
    | head a < head b = head a : merge (tail a) b
    | otherwise = head b : merge a (tail b)


mergeSort :: Ord a => [a] -> [a]
mergeSort a
    | length a < 2 = a
    | otherwise = merge (mergeSort left) (mergeSort right)
        where 
            h = length a `div` 2
            left = take h a
            right = drop h a


-- Function to read and parse the input file into two arrays of numbers
parseInput :: FilePath -> IO ([Int], [Int])
parseInput filename = do
    content <- readFile filename
    let linesOfFile = lines content
    let pairs = map (map read . words) linesOfFile
    let leftNumbers = map (!! 0) pairs
    let rightNumbers = map (!! 1) pairs
    return (leftNumbers, rightNumbers)

-- Function to read smallInput.txt specifically
readInput :: IO ([Int], [Int])
readInput = parseInput "input.txt"


-- Example usage function
partOne :: IO ()
partOne = do
    (left, right) <- readInput
    let sortedLeft = mergeSort left
    let sortedRight = mergeSort right

    let distances = map abs (zipWith (-) sortedLeft sortedRight)
    let totalDistance = sum distances

    putStrLn "Total distance:"
    print totalDistance


count :: Eq a => a -> [a] -> Int
count x = length . filter (==x) 


similarityScores :: Ord a => [a] -> Map.Map a Int
similarityScores a = do
    Map.fromList [(head g, length g) | g <- group (mergeSort a)]

scorer :: Map Int Int -> (Int -> Int)
scorer scoreMap = score
  where
    score key = findWithDefault 0 key scoreMap * key

partTwo :: IO ()
partTwo = do
    (left, right) <- readInput
    let rightScores = similarityScores right

    let scores = map (scorer rightScores) left
    let totalScore = sum scores

    putStrLn "Similariy score: "
    print totalScore

main :: IO ()
main = do
    partOne
    partTwo