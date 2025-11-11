-- Function to read and parse the input file into two arrays of numbers
parseInput :: FilePath -> IO --TODO: Insert output type
parseInput filename = do
    content <- readFile filename
    let linesOfFile = lines content


-- Function to read smallInput.txt specifically
readInput :: IO --TODO: Insert output type
readInput = parseInput "input.txt"


-- Example usage function
partOne :: IO ()
partOne = do
    input <- readInput


partTwo :: IO ()
partTwo = do
    input <- readInput


main :: IO ()
main = do
    partOne
    partTwo