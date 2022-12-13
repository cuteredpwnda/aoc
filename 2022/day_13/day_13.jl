using TimerOutputs

# Part 1
function part1(input)
    for line in input
        # parse the lists in line
        parsed_line = []
        split_line = split(line, ",")
        for (i, char) in enumerate(split_line)
            # check if char is an integer
            if startswith(char, 
                # go pack everything until the next "]" into a list
                rest = split_line[i+1:end]
                closing_bracket = [x for x in rest if endswith(x, "]")][1]
                end_index = findfirst(isequal(closing_bracket), rest)
                # trim the [ and ] from the string
                start_char = split_line[i][2:end]
                end_char = split_line[i+end_index][1:end-1]
                println("start: $start_char, end: $end_char")
                to_add = vcat([start_char], split_line[i+1:i+end_index-2], [end_char])
                push!(parsed_line, to_add)
                # make everything in the list integers
            elseif startswith(char, r"\d") && !endswith(char, "]")
                # pack to list
                push!(parsed_line, [parse(Int, char) ])                
            else
                error("Kaputt, kaputt, kaputt! Got $char to read")
            end
        println(parsed_line)
        end
    end

    return nothing
end

# Part 2
function part2(input)
    return nothing
end

function main()
    input = open(joinpath(@__DIR__, "input", "test_input.txt")) do f
        readlines(f)
    end
    to = TimerOutput()

    @timeit to "part1" p1 = part1(input)
    @timeit to "part2" p2 = part2(input)
    @show p1
    @show p2
    @show to
end

main()