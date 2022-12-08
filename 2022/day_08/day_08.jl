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
            # check if max, set is_visible to true
            left_part = field[j, 1:i-1]
            right_part = field[j, i+1:end]
            top_part = field[1:j-1, i]
            bottom_part = field[j+1:end, i]
            visible_from_left = (maximum(left_part) < item)
            visible_from_right = (maximum(right_part) < item)
            visible_from_top = (maximum(top_part) < item)
            visible_from_bottom = (maximum(bottom_part) < item)
            if visible_from_left || visible_from_right || visible_from_top || visible_from_bottom
                is_visible[j, i] = true
            end
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
            # check if max, set is_visible to true
            left_part = field[j, 1:i-1]
            right_part = field[j, i+1:end]
            top_part = field[1:j-1, i]
            bottom_part = field[j+1:end, i]
            see_left = findfirst([x < item for x in reverse(left_part)].== false)
            see_right = findfirst([x < item for x in right_part].== false)
            see_up = findfirst([x < item for x in reverse(top_part)].== false)
            see_down = findfirst([x < item for x in bottom_part].== false)
            left_score = see_left === nothing ? length(left_part) : see_left
            right_score = see_right === nothing ? length(right_part) : see_right
            top_score = see_up === nothing ? length(top_part) : see_up
            bottom_score = see_down === nothing ? length(bottom_part) : see_down
            score = left_score * right_score * top_score * bottom_score
            scenic_scores[j, i] = score
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