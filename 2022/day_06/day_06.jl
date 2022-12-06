function get_signal_start(signal, start_after)
    for i in eachindex(signal)
        if length(Set(signal[i:(i+start_after-1)])) == start_after
            return i+start_after-1
        end
    end
end

# Part 1
function part1(input)
    get_signal_start(input[1], 4)
end

# Part 2
function part2(input)
    get_signal_start(input[1], 14)
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
        readlines(f)
    end
    @show part1(input)
    @show part2(input) 
end

main()