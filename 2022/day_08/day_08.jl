using DataStructures

function init_matrix(input, pt2=false)
    colsize = length(collect(split(input[1], "")))
    field = zeros(Int64, length(input), colsize)
    if pt2
        m2 = zeros(Int64, length(input), colsize)
    else
        m2 = zeros(Bool, length(input), colsize)
    end
    for (i, line) in enumerate(input)
        row = collect(split(line, ""))
        for (j, c) in enumerate(row)
            field[i, j] = parse(Int64, c)
        end
    end
    return field, m2
end

function print_matrix(m)
    for item in eachrow(m)
        println(item)
    end
end

function partition_views(j::Int64, i::Int64, m::Matrix) :: Tuple{Vector, Vector, Vector, Vector}
    return m[j, 1:i-1], m[j, i+1:end], m[1:j-1, i], m[j+1:end, i]
end

function get_visibility(item::Int64, l::Vector, r::Vector, t::Vector, b::Vector)::Vector{Bool}
    return [(maximum(x) < item) for x in [l, r, t, b]]
end

function find_blocking(item::Int64, l::Vector, r::Vector, u::Vector, d::Vector)::Vector{Union{Int64, Nothing}}
    return [findfirst([x < item for x in z].== false) for z in collect(z in [l, u] ? reverse(z) : z for z in [l, r, u, d])]
end

function calculate_scenic_score(partition::Tuple{Vector, Vector, Vector, Vector}, blocking::Vector{Union{Int64, Nothing}})::Int64
    return prod([y === nothing ? length(x) : y for (x, y) in zip(partition, blocking)])
end

# Part 1
function part1(input)
    field, is_visible = init_matrix(input)
    # for each item, check if each item horizontally and vertically is lower
    for (j, row) in enumerate(eachrow(field))
        for (i, item) in enumerate(row)
            if i == 1 || j == 1 || i == size(field)[1] || j == size(field)[2]
                is_visible[j, i] = true
                continue
            end
            is_visible[j, i] = any(get_visibility(item, partition_views(j, i, field)...)) ? true : false
        end 
    end
    c = counter(is_visible)
    return c[true]
end

# Part 2
function part2(input)
    field, scenic_scores = init_matrix(input, true)
    
    for (j, row) in enumerate(eachrow(field))
        for (i, item) in enumerate(row)
            if i == 1 || j == 1 || i == size(field)[1] || j == size(field)[2]
                scenic_scores[j, i] = 0
                continue
            end
            partition = partition_views(j, i, field)
            scenic_scores[j, i] = calculate_scenic_score(partition, find_blocking(item, partition...))
        end
    end
    return maximum(scenic_scores)
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