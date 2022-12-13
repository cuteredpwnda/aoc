using TimerOutputs
using JSON

function check_order(a, b)
    # check type of a and b
    if typeof(a) == typeof(b) == Int
        # check which value is larger, if equal return nothing
        return a < b ? true : a > b ? false : nothing
    elseif isa(a, Array) && isa(b, Array)
        for i in 1:max(length(a), length(b))
            # check which value is larger, if equal do nothing
            if i > length(a)
                return true
            elseif i > length(b)
                return false
            end
            # recurse on the next values
            if (c = check_order(a[i], b[i])) !== nothing
                return c
            end
        end
    # just one is an array and the other is not
    else 
        if isa(a, Int)
            # put into a list and recurse
            check_order([a], b)
        else # b is an Int
            check_order(a, [b])
        end
    end
end

# Part 1
function part1(input)
    amount = 0
    parsed = []
    for (i, pair) in enumerate(input)
        # use Meta.parse the string into what it resembles as a julia expression
        pair = [eval(Meta.parse(x)) for x in pair]        
        push!(parsed, pair...)
        amount += check_order(pair...) ? i : 0
    end
    return amount
end

# Part 2
function part2(input)
    parsed = []
    for pair in input
        # use Meta.parse the string into what it resembles as a julia expression
        pair = [eval(Meta.parse(x)) for x in pair]
        push!(parsed, pair...)
    end
    divider_packages = [[[2]], [[6]]]
    push!(parsed, divider_packages...)    
    # sort the packages by check_order, funny julia syntax
    sort!(parsed, lt=check_order)
    # find all the indices of the divider packages (should only be 2, but just in case)
    indices = findall(in(divider_packages), parsed)
    println("Indices of divider packages $indices")
    return prod(indices)
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
        split.(split(read(f, String), "\n\n"), "\n")
        #split.(split(read(f, String), "\r\n\r\n"), "\r\n")
    end
    to = TimerOutput()

    @timeit to "part1" p1 = part1(input)
    @timeit to "part2" p2 = part2(input)
    @show p1
    @show p2
    @show to
end

main()