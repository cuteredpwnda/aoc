using DataStructures

function print_matrix(m)
    str = ""
    for (x, item) in enumerate(eachrow(m))
        str *= join(item, " ")
        str *= x==(size(m)[1]) ? "" : "\n"
    end
    return str
end

function init_grid(input)
    grid = Array{Char}(undef, length(input), length(input[1]))
    for (i, row) in enumerate(input)
        for (j, char) in enumerate(row)
            grid[i, j] = char
        end
    end
    return grid
end

function populate_grid(grid, pt2=false)
    queue = Queue{Tuple{Int, Int}}()
    path = Dict{Tuple{Int, Int}, Int}()
    end_x, end_y = 0, 0
    for y in 1:size(grid)[1]
        row = grid[y, :]
        for (x, char) in enumerate(row)
            # replace S with a
            start_points = pt2 ? ['S', 'a'] : ['S']
            if char in start_points
                enqueue!(queue, (x, y))
                path[(x, y)] = 0
                grid[y, x] = 'a'
            elseif char == 'E'
                end_x, end_y = x, y
                grid[y, x] = 'z'
            end
        end
    end
    return queue, path, end_x, end_y
end

function bfs(queue, path, grid, end_x, end_y)
    while length(queue) > 0
        x, y = dequeue!(queue)
        if (x, y) == (end_x, end_y)
            break
        end
        for (next_x, next_y) in [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
            # check if in bounds, not already visited
            in_bounds = (1 <= next_x <= size(grid)[2]) && (1 <= next_y <= size(grid)[1])
            in_keys = ((next_x, next_y) in keys(path))        
            if in_bounds && !in_keys
                # get the values of the chars
                next_v = Int(grid[next_y, next_x])
                curr_v = Int(grid[y, x])
                is_possible = next_v - curr_v <= 1
                if is_possible
                    # check if the difference is max 1
                    enqueue!(queue, (next_x, next_y))
                    path[(next_x, next_y)] = path[(x, y)] + 1
                end
            end
        end
    end
    return path
end
# Part 1
function part1(input)
    grid = init_grid(input)
    queue, path, end_x, end_y = populate_grid(grid)
    path = bfs(queue, path, grid, end_x, end_y)    
    return path[(end_x, end_y)]
end

# Part 2
function part2(input)
    grid = init_grid(input)
    queue, path, end_x, end_y = populate_grid(grid, true)
    path = bfs(queue, path, grid, end_x, end_y)
    return path[(end_x, end_y)]
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