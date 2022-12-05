start_cargo_stacks = Dict{Int, Array{String}}(
    1 => ["F", "T", "C", "L", "R", "P", "G", "Q"],
    2 => ["N", "Q", "H", "W", "R", "F", "S", "J"],
    3 => ["F", "B", "H", "W", "P", "M", "Q"],
    4 => ["V", "S", "T", "D", "F"],
    5 => ["Q", "L", "D", "W", "V", "F", "Z"],
    6 => ["Z", "C", "L", "S"],
    7 => ["Z", "B", "M", "V", "D", "F"],
    8 => ["T", "J", "B"],
    9 => ["Q", "N", "B", "G", "L", "S", "P", "H"]
)

# LIFO or FIFO
function handle_instruction(stacks, amount, from, to, pt2=false)
    if pt2 
        transfer = stacks[from][end-amount+1:end]
        stacks[from] = stacks[from][1:end-amount]
        stacks[to] = vcat(stacks[to], transfer)
    else
        i = 0
        while i < amount
            transfer = pop!(stacks[from])
            stacks[to] = push!(stacks[to], transfer)
            i += 1
        end
    end
end

# parse instructions
function get_instructions(input)::Array{String}
    instructions = []
    for (i, line) in enumerate(input)
        if line == ""
            instructions = input[i+1:end]
            break
        end
    end
    return instructions
end

function parse_instruction(instruction)::Tuple{Int, Int, Int}
    amount = parse(Int, split(match(r"^move \d+", instruction).match, " ")[end])
    from = parse(Int, split(match(r"from \d+", instruction).match)[end])
    to = parse(Int, split(match(r"to \d+", instruction).match)[end])     
    return amount, from, to
end

function collect_result(cargo_stacks)::String
    return join([pop!(x[end]) for x in sort(collect(cargo_stacks), by=x->x[1])])
end

# Part 1
function part1(input)
    # init cargo stacks with start value
    cargo_stacks = deepcopy(start_cargo_stacks)
    for instruction in get_instructions(input)
        handle_instruction(cargo_stacks, parse_instruction(instruction)...)
    end
    return collect_result(cargo_stacks)
end

# Part 2
function part2(input)
    # init cargo stacks with start value
    cargo_stacks = deepcopy(start_cargo_stacks)
    for instruction in get_instructions(input)
        handle_instruction(cargo_stacks, parse_instruction(instruction)..., true)
    end
    return collect_result(cargo_stacks)
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
        readlines(f)
    end
    @show part1(input)
    @show part2(input) 
end

main()