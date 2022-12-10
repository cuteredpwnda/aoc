function print_matrix(m)
    str = ""
    for (x, item) in enumerate(eachrow(m))
        str *= join(item, " ")
        str *= x==(size(m)[1]) ? "" : "\n"
    end
    return str
end

# Part 1
function part1(input)
    x = 1
    sum = 0
    cycle = 1
    for (i, line) in enumerate(input)        
        # try splitting the line at the space
        # if it fails, then it's a noop
        instruction = split(line, " ")
        if instruction[1] == "addx"
            v = parse(Int, instruction[2])
            for _ in 1:2
                if cycle in [20, 60, 100, 140, 180, 220]
                    sum += cycle*x
                end                
                cycle += 1
            end
            x += v
        else # noop
            if cycle in [20, 60, 100, 140, 180, 220]
                sum += cycle*x
            end
            cycle += 1
        end
    end
    return sum
end

function draw_pixel(m, x, y)
    m[y, x] = "#"
end

important_cyles = [1, 40, 41, 80, 81, 120, 121, 160, 161, 200, 201, 240]

function generate_sprite_filling(x)
    if x >= 1
        filling = ""
        for _ in 1:x-1
            filling *= "."
        end
        filling *= "###"
        for _ in x+3:40
            filling *= "."
        end
    elseif x == 0
        filling = "##"
        for _ in 2:40
            filling *= "."
        end
    elseif x == -1
        filling = "#"
        for _ in 2:40
            filling *= "."
        end
    else
        filling = ""
        for _ in 1:40
            filling *= "."
        end
    end
    return filling
end

# Part 2
function part2(input)
    m = Matrix{String}(undef, 6, 40)
    for i in eachindex(m)
        m[i] = "."
    end
    # set the sprite, tuple of the sprite and the index middle of the sprite
    x = 1
    cycle = 1
    # make an array of the sprites
    filling = generate_sprite_filling(x)
    sprite = (filling, x)
    for (i, line) in enumerate(input)
        instruction = split(line, " ")
        if instruction[1] == "addx"
            v = parse(Int, instruction[2])
            filling = generate_sprite_filling(x)
            sprite = (filling, x)
            for j in 1:2
                row = (cycle - 1) ÷ 40 + 1
                x_pos = (cycle - 1) % 40 + 1
                # draw ONE pixel if sprite is on the same index as the pixel to be drawn
                sprite_is_on_pixel = (sprite[1][x_pos] == '#')
                if sprite_is_on_pixel
                    draw_pixel(m, x_pos, row)
                end
                cycle += 1                
            end
            x += v
        else # noop
            filling = generate_sprite_filling(x)
            sprite = (filling, x)
            row = (cycle - 1) ÷ 40 + 1
            x_pos = (cycle - 1) % 40 + 1
            # draw ONE pixel at x-1
            sprite_is_on_pixel = (sprite[1][x_pos] == '#')
            if sprite_is_on_pixel
                draw_pixel(m, x_pos, row)
            end
            cycle += 1
        end
    end
    println("\n===================================== final image =====================================\n")
    println(print_matrix(m))
    return nothing
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
        readlines(f)
    end
    p1 = part1(input)
    @show p1
    part2(input)
end

main()