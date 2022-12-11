using ProgressBars

mutable struct Monkey
    name:: String
    starting_items:: Vector{Int128}
    operation:: Tuple{String, String} # what to do with the items, multiply or add the value
    test:: Tuple{Int128, Dict{Bool, String}} # which monkey to throw to if true or false, checks if divisible by first int
end
Base.show(io::IO, m::Monkey) = print(io, "Monkey: $(m.name)\n  starting_items: $(m.starting_items)\n  operation: $(m.operation)\n  test: $(m.test)")

uint_max = typemax(UInt128)
int_max = typemax(Int128)
println("uint_max: $uint_max")
println("int_max: $int_max")

function play_round(monkeys::Array{Monkey}, inspections::Dict{String, Int128}, pt2=false)
    mod = prod([monkey.test[1] for monkey in monkeys])
    for monkey in monkeys
        # set the number of inspections to 0
        # get the items
        items = monkey.starting_items
        #println("$(monkey.name) holds $(items)")
        while length(items) > 0
            # monkey inspects item
            inspections[monkey.name] += 1
            worry_level = items[1]
            #println("  Monkey inspects an item with a worry level of $worry_level.")
            # println("operation: ", monkey.operation)
            if monkey.operation[2] == " old"
                num = worry_level
            else
                num = parse(Int128, monkey.operation[2])
            end
            if monkey.operation[1] == "*"
                worry_level *= num
            else
                worry_level += num
            end
            #println("    Worry level increases by $num to $worry_level.")
            # monkey gets bored
            if !pt2
                worry_level ÷= 3
            end
            #println("    Monkey gets bored with item. Worry level is divided by 3 to $worry_level.")
            # check if divisible by the int
            # println("test: ", monkey.test)
            # make sure the worry level is not too big
            worry_level = pt2 ? worry_level % mod : worry_level
            divisible_by = monkey.test[1]
            test = worry_level % divisible_by == 0
            #println("    Current worry level is divisible by $divisible_by: $test.")
            throw_to = monkey.test[2][test]
            # println("throw to: ", throw_to)
            get_monkey_index = parse(Int128, split(throw_to, " ")[end])
            #println("    $(monkey.name) throws $worry_level to Monkey $(get_monkey_index)")
            push!(monkeys[get_monkey_index+1].starting_items, worry_level)
            popat!(items, 1)
        end
    end
    
    # println("=====================================")
    # println("Monkeys have finished their round.")
    # println("They are now holding:")
    # for monkey in monkeys
    #     println("$(monkey.name) $(monkey.starting_items)")
    # end
    
end

function init_monkeys(input) :: Array{Monkey}
    # sperate the input into the monkeys
    monkeys = Array{Monkey}(undef, 0)
    for (i, line) in enumerate(input)
        if line == ""
            continue
        end
        if startswith(line, "Monkey")
            # create a new monkey
            monkey = Monkey(line, [], ("", ""), (0, Dict{Bool, String}()))
            push!(monkeys, monkey)
            curr_monkey = monkey

            # split the line into the starting items
            split_line = split(input[i+1], ":")
            starting_items = [parse(Int128, x) for x in split(split_line[2], ",")]
            curr_monkey.starting_items = starting_items
            
            # split the line into the operation
            split_line = split(input[i+2], "=")
            split_again = split(split_line[2], r"(\+|\*)")            
            op = split(split_line[2], " ")[end-1]
            operation = (op, split_again[end])
            curr_monkey.operation = operation

            # split the line into the test
            split_line = split(input[i+3], ":")
            split_again = split(split_line[2], " ")
            true_line = split(input[i+4], " to ")
            false_line = split(input[i+5], " to ")
            test = (parse(Int128, split_again[end]),
                    Dict{Bool, String}( true =>  true_line[end],
                                        false => false_line[end]))
            curr_monkey.test = test
            i+=5
        end
    end
    # sort the monkeys by name
    return collect(sort(monkeys, by=x -> x.name))
end

# Part 1
function part1(input)
    monkeys = init_monkeys(input)
    # init inspections dict
    inspections = Dict{String, Int128}()
    for monkey in monkeys
        inspections[monkey.name] = 0
    end

    for _ in 1:20
        play_round(monkeys, inspections)
        #println("Inspections: ", inspections)
    end
    # get the two monkeys with the most items inspected
    sorted = sort(collect(inspections), by=x -> x[2], rev=true)
    return sorted[1][2] * sorted[2][2]
end

# Part 2
function part2(input)
    monkeys = init_monkeys(input)
    # init inspections dict
    inspections = Dict{String, Int128}()
    for monkey in monkeys
        inspections[monkey.name] = 0
    end

    for i in ProgressBar(1:10000)
        play_round(monkeys, inspections, true)
        # if i in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
        #     println("After round $i\n", sort(collect(inspections), by = x -> x[1]))
        # end
    end
    # get the two monkeys with the most items inspected
    sorted = sort(collect(inspections), by=x -> x[2], rev=true)
    return sorted[1][2] * sorted[2][2]
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
        readlines(f)
    end
    p1 = part1(input)
    p2 = part2(input)
    @show p1
    @show p2
end

main()