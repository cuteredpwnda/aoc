using TimerOutputs
using LinearAlgebra

function print_matrix(m)
    str = ""
    for (x, item) in enumerate(eachrow(m))
        str *= join(item, "")
        str *= x==(size(m)[1]) ? "" : "\n"
    end
    return str
end


function manhattan(p1, p2)
    return trunc(Int, norm(p1 .- p2, 1))
end
# Part 1
function part1(input)
    #test_line = 2000000
    test_line = 10
    y_set = Set()
    beacons_x_at_y = Set()
    for line in input
        sensor_at, closest_at = split(line, ": ")
        s = [x for x in split(sensor_at, "=")]
        c = [x for x in split(closest_at, "=")]
        s_x, s_y = parse(Int, split(s[end-1], ", ")[1]), parse(Int, s[end])
        b_x, b_y = parse(Int, split(c[end-1], ", ")[1]), parse(Int, c[end])
        b_y == test_line ? push!(beacons_x_at_y, b_x) : nothing
        # calc manhattan
        md = manhattan((s_x, s_y), (b_x, b_y))
        # subtract how far away the sensor is on the y axis because we only need the extend on the x axis
        md -= abs(test_line - s_y)
        x = s_x
        for x in (s_x - md):(s_x + md)
            push!(y_set, x)
        end
    end
    return length(setdiff(y_set, beacons_x_at_y))
end

# Part 2
function part2(input)
    max_x = 4000000
    # create an array for each columns
    range = [[] for _ in 1:max_x+1]
    
    for line in input
        sensor_at, closest_at = split(line, ": ")
        s = [x for x in split(sensor_at, "=")]
        c = [x for x in split(closest_at, "=")]
        s_x, s_y = parse(Int, split(s[end-1], ", ")[1]), parse(Int, s[end])
        b_x, b_y = parse(Int, split(c[end-1], ", ")[1]), parse(Int, c[end])

        # calc manhattan
        md = manhattan((s_x, s_y), (b_x, b_y))
        delta_y = 0

        while md > 0
            left_x = max(0, s_x - md)
            right_x = min(max_x, s_x + md)
            (s_y - delta_y >= 0) ? push!(range[s_y - delta_y+1], [left_x, right_x]) : nothing
            (s_y + delta_y <= max_x) ? push!(range[s_y + delta_y+1], [left_x, right_x]) : nothing
            delta_y +=1
            md -=1
        end
    end
    range = [unique(x) for x in range] 
    pos_x = 0
    y = 1
    pos_y = undef
    for y in 1:max_x+1
        if y >= length(range)
            continue
        end
        xs = range[y]
        sort!(xs, by=x->x[1])
        if xs[1][1] != 0
            pos_x = 0
            pos_y = y-1
            break
        end
        last = xs[1][2]
        for i in 2:length(xs)
            if (last >= xs[i][1]-1)
                last = max(last, xs[i][2])
            else
                pos_y = y-1
                break
            end
        end
        if (last != max_x)
            pos_x = last + 1
            pos_y = y-1
            break
        end
        y+=1
    end
    return max_x * pos_x + pos_y
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
        readlines(f)
    end
    to = TimerOutput()

    @timeit to "part1" p1 = part1(input)
    @show p1
    @timeit to "part2" p2 = part2(input)
    @show p2
    @show to
end

main()