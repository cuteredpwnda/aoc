# Part 1
function part1(input)
    for (i, char) in enumerate(input[1])
        window = input[1][i:i+3]
        unique_chars = Set(window)
        if length(unique_chars) == 4
            signal_start = i+3
            return signal_start
        end
    end
end

# Part 2
function part2(input)
    for (i, char) in enumerate(input[1])
        window = input[1][i:i+13]
        unique_chars = Set(window)
        if length(unique_chars) == 14
            signal_start = i+13
            return signal_start
        end
    end
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
        readlines(f)
    end
    @show part1(input)
    @show part2(input) 
end

main()