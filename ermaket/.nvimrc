"let test#python#pytest#options = '--pudb'
let test#python#pytest#options = '--capture=no'
let g:ale_linters = {'vue': ['vls'], 'typescript': ['tsserver', 'tslint'], 'python': ['pyls']}
let g:ale_pattern_options = {
            \ '.*\.tmpl\.py$': {'ale_enabled': 0},
            \ }
