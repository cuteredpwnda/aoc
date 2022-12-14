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
    range = max_x - min_x + 1
    cave = Matrix{Char}(undef, max_y+1, range)
    # init with air
    for i in 1:max_y+1
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
    # draw bottom row for pt2
    if pt2
        for i in 1:range
            cave[max_y+1, i] = '#'
        end
    end
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
    
    precon_left ? println("Precon left for $sand_pos") : nothing
    precon_right ? println("Precon right for $sand_pos") : nothing
    if precon_left || precon_right
        cave[sand_pos...] = '.'
        return true
    else 
        precon_saturated = (cave[look_left...] == 'o' &&
                        cave[look_right...] == 'o' &&
                        cave[look_down...] == 'o' &&
                        cave[sand_pos...] == 'o' &&
                        sand_pos == sand_start)
        precon_saturated ? println("Precon saturated for $sand_pos") : nothing        
        if precon_saturated
            # draw last sand grain
            cave[sand_pos...] = 'o'
            return true
        end
    end

    precon_rock_bottom = look_down[1] >= size(cave)[1]
    precon_rock_bottom ? println("Precon bottom for $sand_pos") : nothing
    if precon_rock_bottom && !precon_left && !precon_right
        cave[sand_pos...] = 'o'
        return drop_sand(sand_start, sand_start, cave)
    end

    #check if sand hits sand or rock
    if cave[look_down...] == '#' || cave[look_down...] == 'o'
        # check if left+down is sand or rock
        if cave[look_left...] == '#' || cave[look_left...] == 'o'
            # check if right+down is sand or rock
            if cave[look_right...] == '#' || cave[look_right...] == 'o'
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
    max_x, min_x , max_y, paths = get_dimensions(input)    
    #println("$max_x, $min_x, $max_y")
    cave = init_cave(min_x, max_x, max_y, paths)
    sand_start = (1, 500-min_x+1)
    cave[sand_start...] = '+'
    stop = false
    sand_pos = sand_start
    #println("Starting pos: $sand_pos")
    while stop == false
        stop = drop_sand(sand_start, sand_pos, cave)
    end
    println(print_matrix(cave))
    c = counter(cave)
    return c['o']
end

# Part 2
function part2(input)
    println("========== Part 2 ==========")  
    max_x, min_x , max_y, paths = get_dimensions(input)
    println("pt2: max x: $max_x, min x: $min_x, max y: $max_y")
    
    inf_max_y = max_y + 2
    # make cave infinitely large in x direction, maximum x can be + inf_max_y
    inf_min_x = min_x - inf_max_y
    inf_max_x = max_x + inf_max_y
    
    println("max x: $inf_max_x, min x: $inf_min_x, max y: $inf_max_y")
    cave = init_cave(inf_min_x, inf_max_x, inf_max_y, paths, true)
    println(print_matrix(cave))
    println(size(cave))

    sand_start = (1, 500-inf_min_x+1)
    cave[sand_start...] = '+'
    
    stop = false
    sand_pos = sand_start
    while stop == false
        stop = drop_sand(sand_start, sand_pos, cave)
    end
    println(print_matrix(cave))
    c = counter(cave)
    return c['o']
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