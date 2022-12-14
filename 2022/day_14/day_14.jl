using TimerOutputs
using DataStructures

function print_matrix(m)
    str = ""
    for (x, item) in enumerate(eachrow(m))
        str *= join(item, "")
        str *= x==(size(m)[1]) ? "" : "\n"
    end
    return str
end

# init cave with dynamic size
function init_cave(min_x, max_x, max_y, paths, pt2=false)
    max_y = pt2 ? max_y+3 : max_y+1
    range = max_x - min_x + 1
    cave = Matrix{Char}(undef, max_y, range)
    # init with air
    for i in 1:max_y
        for j in 1:range
            cave[i, j] = '.'
        end
    end
    # draw rock paths
    for path in paths
        for (i, subdiv) in enumerate(path)
            if i == length(path)
                break
            end
            x_1 = parse(Int, subdiv[1]) - min_x + 1
            y_1 = parse(Int, subdiv[2]) + 1
            x_2 = parse(Int, path[i+1][1]) - min_x + 1
            y_2 = parse(Int, path[i+1][2]) + 1
            s_x = x_1 <= x_2 ? 1 : -1
            s_y = y_1 <= y_2 ? 1 : -1
            r_x = s_x == -1 ? (x_1:s_x:x_2) : (x_1:x_2)
            r_y = s_y == -1 ? (y_1:s_y:y_2) : (y_1:y_2)
            for x in r_x
                for y in r_y
                    cave[y, x] = '#'
                end
            end
        end
    end
    if pt2
        # add bottom
        for i in 1:range
            cave[max_y, i] = '#'
        end
    end
    sand_start = (1, 500-min_x+1)
    cave[sand_start...] = '+'
    return cave
end

function drop_sand(sand_start, sand_pos, cave) :: Bool
    look_down = (sand_pos[1]+1, sand_pos[2])
    look_left = (look_down[1], sand_pos[2]-1)
    look_right = (look_down[1], sand_pos[2]+1)
    cave[sand_pos...] = cave[sand_pos...] == '+' ? '+' : 'o'

    
    # check if the sand flows out of the cave
    precon_left = look_left[1] > size(cave)[1] || look_left[2] > size(cave)[2] || look_left[2] < 1    
    precon_right = look_right[1] > size(cave)[1] || look_right[2] > size(cave)[2] || look_right[2] < 1
    if precon_left || precon_right
        cave[sand_pos...] = '.'            
        println("Aborting: ran out of cave")
        return true
    end

    #check if sand hits sand or rock
    down_populated = cave[look_down...] == '#' || cave[look_down...] == 'o'
    left_populated = cave[look_left...] == '#' || cave[look_left...] == 'o'
    right_populated = cave[look_right...] == '#' || cave[look_right...] == 'o'
    if down_populated
        # check if left+down is sand or rock
        if left_populated
            # check if right+down is sand or rock
            if right_populated
                # drop next grain of sand
                return drop_sand(sand_start, sand_start, cave)
            else
                # move right+down
                cave[sand_pos...] = '.'
                sand_pos = look_right
            end
        else
            # move left+down
            cave[sand_pos...] = '.'
            sand_pos = look_left
        end
    else
        # move down
        cave[sand_pos...] = cave[sand_pos...] == '+' ? '+' : '.'
        sand_pos = look_down
    end
    return drop_sand(sand_start, sand_pos, cave)
end

function drop_sand_2() :: Bool
    
end

function get_dimensions(input)
    paths = []
    max_x = 0
    min_x = typemax(Int)
    max_y = 0
    for line in input
        path = split(line, " -> ")
        subdivisions = [split(x, ',') for x in path]
        # get max and min x and max y for the cave and init grid
        max_x = max(max_x, maximum([parse(Int, x[1]) for x in subdivisions]))
        min_x = min(min_x, minimum([parse(Int, x[1]) for x in subdivisions]))
        max_y = max(max_y, maximum([parse(Int, x[2]) for x in subdivisions]))
        push!(paths, subdivisions)
    end
    return max_x, min_x, max_y, paths
end
# Part 1
function part1(input)
    max_x, min_x, max_y, paths = get_dimensions(input)
    #println("$max_x, $min_x, $max_y")
    min_x -= (1 + max_y)
    max_x += (1 + max_y)
    cave = init_cave(min_x, max_x, max_y, paths)
    #println(print_matrix(cave))    
    #println(size(cave))
    s_cart = findfirst(x -> x == '+', cave)
    sand_start = (s_cart[1], s_cart[2])
    stop = false
    sand_pos = sand_start

    #println("Starting pos: $sand_pos")
    drop_sand(sand_start, sand_pos, cave)
    println(print_matrix(cave))
    c = counter(cave)
    return c['o']
end

# Part 2
function part2(input)
    println("====== Part 2 ======")
    # create a set
    sand_coords = Set{Tuple{Int, Int}}()
    # handle input and add to set
    for line in split.(input," -> ")
        coords = [parse.(Int, split(x, ",")) for x in line]
        for (from, to) in zip(coords[2:end], coords)
            from[1] == to[1] && union!(sand_coords, [(from[1], y) for y in from[2]:cmp(to[2], from[2]):to[2]])
            from[2] == to[2] && union!(sand_coords, [(x, from[2]) for x in from[1]:cmp(to[1], from[1]):to[1]])
        end
    end
    println(sand_coords)
    depth = maximum(x->x[2], sand_coords) + 1
    rock_elements = length(sand_coords)
    while !((500, 0) in sand_coords)
        start = (500, 0)
        while true
            if start[2] == depth
                # is at start position
                push!(sand_coords, start)
                break
            elseif !(start.+(0, 1) in sand_coords)
                # check down
                start = start.+(0, 1)
            elseif !(start.+(-1, 1) in sand_coords)
                # check left
                start = start.+(-1, 1)
            elseif !(start.+(1, 1) in sand_coords)
                # check right
                start = start.+(1, 1)
            else
                # if final resting place
                push!(sand_coords, start)
                break
            end
        end
    end
    return length(sand_coords)-rock_elements
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
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