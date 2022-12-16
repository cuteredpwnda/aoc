using TimerOutputs
using Parameters

function print_matrix(m)
    str = ""
    for (x, item) in enumerate(eachrow(m))
        str *= join(item, "\t")
        str *= x==(size(m)[1]) ? "" : "\n"
    end
    return str
end

@with_kw mutable struct Valve
    name::String
    flow_rate::Int
    tunnels::Vector = []
    open::Bool = false
end
Base.show(io::IO, s::Valve) = print(io,"""
    Valve: $(s.name)
    Flow Rate: $(s.flow_rate)
    Open: $(s.open)
    Tunnels: $(s.tunnels)
    """)

function search_valve(valves::Array{Valve}, name::String)::Valve
    for valve in valves
        if valve.name == name
            return valve
        end
    end
    return error("Valve not found")
end

@with_kw mutable struct State
    valves::Vector{Valve}
    time_left::Int
    time_used::Int
    current_action::Union{String, Nothing} = nothing
    looking_at::Union{Valve, Nothing} = nothing
    next_valves::Vector{Valve} = []
end

function get_open_valves(s::State) :: String
    f = filter(x->x.open, s.valves)
    if length(f) == 1
        valve = f[1]
        return "Valve $(valve.name) is open, releasing $(valve.flow_rate) pressure"
    elseif length(f) > 1
        str = "Valves "
        pressure = 0
        for valve in f
            str *= "$(valve.name), "
            pressure += valve.flow_rate
        end
        str *= "are open, releasing $pressure pressure."
        return str
    else
        return "No valves are open."
    end
end

function get_current_action(s::State) :: String
    a = s.current_action
    v = s.looking_at
    if a == "open"
        return "You open valve $(v.name)."
    elseif a == "move"
        return "You move to valve $(v.name)."
    elseif a === nothing
        return "You are not doing anything, quick do something!"
    else
        return error("Unknown action")
    end    
end

Base.show(io::IO, s::State) = print(io,"""
== Minute $(s.time_used) ==
$(get_open_valves(s))
$(get_current_action(s))
""")

function parse_input(input)
    valves = Array{Valve}(undef, 0)
    for line in input
        v, t = split(line, "; ")
        valve = Valve(name=split(v, " ")[2], flow_rate=parse(Int, split(v, "=")[end]))
        valve.tunnels = split(join(split(t, r"valve(s)* ")[2:end]), ", ")
        push!(valves, valve)
    end
    return valves
end

function floyd_warshall(weights, nvert::Int)
    println("Weights:\n", print_matrix(weights), "\nSize 1: $(size(weights, 1)), \n nvert: $nvert")
    dist = fill(Inf, nvert, nvert)
    for i in 1:size(weights, 1)
        dist[weights[i, 1], weights[i, 2]] = weights[i, 3]
    end
    # return dist
    next = collect(j != i ? j : 0 for i in 1:nvert, j in 1:nvert)

    for k in 1:nvert, i in 1:nvert, j in 1:nvert
        if dist[i, k] + dist[k, j] < dist[i, j]
            dist[i, j] = dist[i, k] + dist[k, j]
            next[i, j] = next[i, k]
        end
    end

    # return next
    function printresult(dist, next)
        println("pair     dist    path")
        for i in 1:size(next, 1), j in 1:size(next, 2)
            if i != j
                u = i
                path = "$i -> $j    $(dist[i, j])     $i"
                while true
                    u = next[u, j]
                    path *= " -> $u"
                    if u == j break end
                end
                println(path)
            end
        end
    end
    printresult(dist, next)
end

# Part 1
function part1(input)
    valves = parse_input(input)
    state = State(valves=valves, time_left=30, time_used=0, looking_at=valves[1])
    println("Initial state: ", state)
    max_tunnels = maximum(x->length(x.tunnels), valves)
    weights = fill!(Matrix{Int}(undef, length(valves)*max_tunnels, 3), 0)
    test_matrix = [1 3 -2; 2 1 4; 2 3 3; 3 4 2; 4 2 -1]
    println(print_matrix(test_matrix), "\n")

    j = 0
    for (i, valve) in enumerate(valves)
        for tunnel in valve.tunnels
            to = findfirst(x->x.name==tunnel, valves)
            weights[i+j, 1] = i
            weights[i+j, 2] = to
            weights[i+j, 3] = valves[to].flow_rate
            j+=1
        end
    end
    # remove all rows with 0@weights[i][1]
    weights = weights[weights[:, 1].!=0, :]
    println(print_matrix(weights))    

    #floyd_warshall(test_matrix, 4)

    println()
    # get all possible valve paths
    floyd_warshall(weights, length(valves))

    
    

    while state.time_left > 0   
        state.time_left -= 1
        state.time_used += 1
        #println(state)
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