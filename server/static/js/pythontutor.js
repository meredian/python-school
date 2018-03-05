$(function() {
    window.makeCodeBlocks = function(selector) {
        $(selector).find('.lesson_code').each(function(i, code_block) {
            code_block = $(code_block);

            var executable = code_block.data('executable');

            var code = code_block.find('.code')[0].textContent.trim();
            code_block.find('.code').remove();

            var stdin = '';
            if(executable) {
                stdin = code_block.find('.stdin')[0].textContent.trim();
                code_block.find('.stdin').remove();
            }

            visualizers.push(new Visualizer(code_block, code, stdin, {
                executable: executable,

                auto_height: true,
                show_stdin: (stdin != ''),
                show_stdin_initially: false,

                code_read_only: code_block.data('readonly'),
                stdin_read_only: code_block.data('readonly'),

                explain_mode: false,
                dataviz_enabled: code_block.data('dataviz')
            }));
        });
    };
});