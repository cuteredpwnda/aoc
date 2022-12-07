mutable struct Directory
    dirname :: String
    content :: Array{String}
    files :: Array{String}
    parent :: Union{Directory, Nothing}
    child_dirs :: Array{Directory}
end

Base.show(io::IO, s::Directory) = print(
io,"""
Directory: $(s.dirname)
Content: $(s.content)
Files: $(s.files)
Parent: $(s.parent === nothing ? "None" : s.parent.dirname)
Child Directories: $([x.dirname for x in s.child_dirs])
"""
)

# Part 1
function part1(input)
    directories = []
    parent_dir = nothing
    curr_dir = nothing
    base_dir = directory = Directory("\\", [], [], parent_dir, [])
    # get subdirectories and files
    for (i, line) in enumerate(input)
        new_dir = match(r"^\$ cd ", line)
        ls = match(r"^\$ ls", line)
        if new_dir !== nothing
            dir_name = split(line, " ")[end]
            directory = Directory(dir_name, [], [], parent_dir, [])
            # set as current directory
            curr_dir = directory
        end
        # list contents of directory
        if ls !== nothing
            possible_dir_contents = input[i+1:end]
            max_index = length(possible_dir_contents)
            for (j, content) in enumerate(possible_dir_contents)
                if match(r"\$", content) !== nothing
                    max_index = j
                    break
                end
            end
            content = possible_dir_contents[1:max_index-1]
            curr_dir.content = content
            println(curr_dir)
            # get size of files in dir
            for item in curr_dir.content
                is_file = match(r"\d+", item)
                is_dir = match(r"dir ", item)
                if is_file !== nothing
                    push!(curr_dir.files, item)
                end
            end
        end
    end
    println(directories)
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
    @show part1(input)
    @show part2(input) 
end

main()