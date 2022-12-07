struct File
    filename :: String
    size :: Int64
end
Base.show(io::IO, f::File) = print(
io,"- $(f.filename) (file, size=$(f.size))"
)
mutable struct Directory
    dirname :: String
    content :: Union{Array{String}, Nothing}
    files :: Union{Array{File}, Nothing}
    parent :: Union{Directory, Nothing}
    child_dirs :: Union{Array{Directory}, Nothing}
end


Base.show(io::IO, s::Directory) = print(
io,"""
Directory: $(s.dirname) (dir)
Content: $(s.content === nothing ? "None" : s.content)
Files: $(s.files === nothing ? "None" : [s.filename for s in s.files])
Parent: $(s.parent === nothing ? "None" : s.parent.dirname)
Child Directories: $(s.child_dirs === nothing ? "None" : [x.dirname for x in s.child_dirs])
"""
)

function get_subdirs(dir::Directory) :: Array{Directory}
    subdirs = []
    for item in dir.content
        is_dir = match(r"dir ", item)
        if is_dir !== nothing
            dir_name = split(item, " ")[end]
            directory = Directory(dir_name, nothing, nothing, dir, nothing)
            push!(subdirs, directory)
        end
    end
    return subdirs
end

function get_content(possible_dir_contents::Array) :: Array{String}
    max_index = length(possible_dir_contents)
    for (j, content) in enumerate(possible_dir_contents)
        m = match(r"^\$ ", content)
        # check if new command
        if  m !== nothing
            max_index = j
            break
        end
    end
    return possible_dir_contents[1:max_index-1]
end

# Part 1
function part1(input)
    directories = []
    base_dir = Directory("\\", nothing, nothing, nothing, nothing)
    parent_dir = base_dir
    curr_dir = base_dir
    push!(directories, base_dir)
    # get subdirectories and files
    for (i, line) in enumerate(input[2:end])
        ls = match(r"^\$ ls", line)
        cd = match(r"^\$ cd", line)
        # list contents of directory
        if ls !== nothing
            possible_dir_contents = input[i+2:end]
            curr_dir.content = get_content(possible_dir_contents)
            #println("dir: $(curr_dir.dirname)\n  content: $(curr_dir.content)")
            # get size of files in directory
            for item in curr_dir.content
                is_file = match(r"\d+", item)
                is_dir = match(r"dir ", item)
                if is_file !== nothing
                    fn = split(item, " ")[end]
                    file = File(fn, parse(Int64, is_file.match))
                    if curr_dir.files === nothing                        
                        curr_dir.files = [file]
                    else
                        push!(curr_dir.files, file)
                    end
                end
                if is_dir !== nothing
                    dir_name = split(item, " ")[end]
                    directory = Directory(dir_name, nothing, nothing, curr_dir, nothing)
                    if curr_dir.child_dirs === nothing
                        curr_dir.child_dirs = [directory]
                    else
                        push!(curr_dir.child_dirs, directory)
                    end
                end
            end
            i += length(curr_dir.content)
        end
        # if directory changes
        if cd !== nothing
        end
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
    @show part1(input)
    @show part2(input) 
end

main()