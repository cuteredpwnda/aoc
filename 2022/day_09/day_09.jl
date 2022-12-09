using DataStructures
using ProgressBars
using ProgressLogging
using Parameters

function print_matrix(m)
    str = ""
    for (x, item) in enumerate(eachrow(m))
        str *= join(item, " ")
        str *= x==(size(m)[1]) ? "" : "\n"
    end
    return str
end

@with_kw mutable struct Snek
    head :: Char = 'H'
    tail :: Union{Char, Nothing} = nothing
    elements :: Array{Char} = []
end
Base.show(io::IO, s::Snek) = print(io," ~<($(s.head))$(s.elements !== nothing ? s.elements : "")>")

mutable struct State
    command :: String
    field :: Union{Matrix{Char}, Nothing}
    visited :: Union{Matrix{Char}, Nothing}
    covers :: Array{Char}
    snake :: Union{Snek, Nothing}
end

Base.show(io::IO, s::State) = print(
io,"""
== $(s.command) == 
$(print_matrix(s.field))\t($(s.covers))
visited matrix:
$(print_matrix(s.visited))
current snake: $(s.snake)
"""
)

function check_adjacent(m::Matrix{Char}) :: Bool
    # check if the tail pulls back the head, check if they are adjacent
    head = findfirst(x->x=='H', m)
    tail = findfirst(x->x=='T', m)
    if length(tail) == 0 
        return true
    end
    condition = (abs(head[1] - tail[1]) <= 1) && (abs(head[2] - tail[2]) <= 1)
    if condition
        return true
    end    
    return false
end

function move(direction::Char, value::Int, state::State, debug::Bool=false)
    # dir = [up/down, left/right]
    if direction == 'R'
        dir = [0, 1]        
    elseif direction == 'L'
        dir = [0, -1]
    elseif direction == 'U'
        dir = [-1, 0]
    elseif direction == 'D'
        dir = [1, 0]
    else
        error("Unknown direction")
    end
    # actually move
    to_move = value
    while to_move > 0
        # move the head, check if the tail pulls back the head
        curr_head = findfirst(x->x=='H', state.field)
        new_head = curr_head[1]+(1*dir[1]), curr_head[2]+(1*dir[2])
        pushed_tail = false
        if state.field[new_head...] == 'T'
            # if the field is occupied by the tail, push the tail to the covers
            push!(state.covers, 'T')
            pushed_tail = true
            state.field[curr_head[1], curr_head[2]] = '.' # clear the field
        end
        state.field[new_head...] = 'H'
        curr_tail = findfirst(x->x=='T', state.field)
        if !pushed_tail
            state.field[curr_head[1], curr_head[2]] = state.covers != [] ? pop!(state.covers) : '.'
        else 
            state.visited[new_head[1], new_head[2]] = '#' # mark the field as visited again
        end
        if curr_tail !== nothing
            if !check_adjacent(state.field)
                # pull the tail if it is not adjacent to the head anymore
                state.field[curr_head[1], curr_head[2]] = 'T'
                new_tail = curr_head
                con = new_tail != curr_tail
                if con
                    state.field[curr_tail[1], curr_tail[2]] = '.' # clear the field
                    state.visited[curr_tail[1], curr_tail[2]] = '#' # mark the field as visited
                    state.field[new_tail[1], new_tail[2]] = 'T'
                end
            end
        end
        to_move -= 1
        debug ? println("Field after moving ($to_move/$value) in $direction:\n$(print_matrix(state.field))") : nothing
        debug ? println("Visited:\n$(print_matrix(state.visited))") : nothing
    end
end

function check_adjacent(m::Matrix{Char}, c1::Char, c2::Char) :: Bool
    # check if the tail pulls back the head, check if they are adjacent
    head = findfirst(x->x==c1, m)
    tail = findfirst(x->x==c2, m)
    if tail === nothing || head === nothing
        return false
    end
    if length(tail) == 0
        return true
    end
    condition = (abs(head[1] - tail[1]) <= 1) && (abs(head[2] - tail[2]) <= 1)
    if condition
        return true
    end    
    return false
end

function get_next_move(h, t)
    # map the elements h and t to the direction they should move
    # move the maximum change, if the maximum change is 0, don't move

    return maximum(abs.(h .- t)) > 1 ? map(x -> sign(x), h .- t) : (0, 0)
end

# dir = [up/down, left/right]
dir = Dict('R' => (1, 0), 'L' => (-1, 0), 'U' => (0, 1), 'D' => (0, -1))

function init_state(input, state)
    # get the maximum size of the matrix
    x, y = 1, 1
    println("calculating the size of the matrix...")
    commands = [(d = line[1], v = parse(Int, line[2:end])) for line in input]
    c =  counter([x.d for x in commands])
    max_in_x = maximum([x.v for x in commands if x.d in ['R', 'L']])
    max_in_y = maximum([x.v for x in commands if x.d in ['U', 'D']])
    x = ((c['R'] + c['L']) ÷ 2 + max_in_x)
    y = ((c['U'] + c['D']) ÷ 2 + max_in_y)
    # initialize the matrix with the size of half of the maximum size  
    println("initializing matrix")
    m = Array{Char}(undef, y*2, x*2) # TODO check the size of the matrix
    println("setting everything to '.'")
    for i in ProgressBar(eachindex(m))
        m[i] = '.'
    end
    println("creating a second matrix for the visited matrix")
    v = deepcopy(m)
    state.field = m
    state.visited = v
end

state_pt1 = State("Initial State", nothing, nothing, ['T'], nothing)
snek = Snek('H', nothing, ['H'])
state_pt2 = State("Initial State Part 2", nothing, nothing, reverse!(['1', '2', '3', '4', '5', '6', '7', '8', '9']), snek)

# Part 1
function part1(input)
    init_state(input, state_pt1)
    debug = (size(state.field) < (20, 20) ? true : false)
    # set the head as center of the matrix    
    center = ((size(state_pt1.field)[1]+1) ÷ 2 , (size(state_pt1.field)[2]+1) ÷ 2)
    debug ? println("center: $center") : nothing
    state_pt1.field[center...] = 'H'
    debug ? println(state) : nothing
    debug ? println("iterating over the input to move the rope") : nothing
    for i in ProgressBar(eachindex(input[1:2]))
        line = input[i]
        direction, value = line[1], parse(Int, line[2:end])
        state_pt1.command = "$direction $value"
        move(direction, value, state_pt1, debug)
        if state_pt1.field[center...] == '.'
            state_pt1.field[center...] = 's'
        end
    end
    # for the final state, set T's index in visited to '#'
    tail = findfirst(x->x=='T', state_pt1.field)
    state_pt1.visited[tail] = '#'
    state_pt1.command = "Final state"
    debug ? println(state_pt1) : nothing
    c =  counter(state_pt1.visited)
    println(c)
    return c['#']
end

# Part 2
function part2(input, pt1=false)
    snek_length = pt1 ? 2 : 10
    knot_matrix = [(0,0) for _ in 1:snek_length]
    # prepare a set of visited points
    visited = Set()
    # split all lines at the space
    lines = split.(input, " ")
    for line in lines
        # get the value to move, move in steps of 1
        for _ in 1:parse(Int, line[2])
            # move the head +1 in the direction of the line (get the char)
            knot_matrix[1] = knot_matrix[1] .+ dir[line[1][1]]
            # move the rest of the snake
            for knot in 2:snek_length
                next_move = get_next_move(knot_matrix[knot-1], knot_matrix[knot])
                knot_matrix[knot] = knot_matrix[knot] .+ next_move
            end
            push!(visited, knot_matrix[snek_length])
        end
    end
    return length(visited)
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
        readlines(f)
    end
    p1 = part2(input, true)
    p2 = part2(input)
    @show p1
    @show p2
end

main()