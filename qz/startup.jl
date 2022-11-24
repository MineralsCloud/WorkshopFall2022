using OhMyREPL
colorscheme!("Monokai16")
enable_autocomplete_brackets(false)

using InteractiveUtils: supertypes
const co = collect
const st = supertypes
const et = eltype
const to = typeof
const mo = methods
const fn = fieldnames
const len = length
using TypeTree: tt

# See https://github.com/JuliaLang/julia/issues/29223#issuecomment-934256942
macro showall(expr)
    return quote
        show(IOContext(stdout, :compact => false, :limit => false), "text/plain", $(esc(expr)))
    end
end
