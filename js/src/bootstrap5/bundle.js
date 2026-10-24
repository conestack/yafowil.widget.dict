import $ from 'jquery';
import { DictWidget, register_array_subscribers } from './widget.js';

export * from './widget.js';

$(() => {
    if (window.ts !== undefined) {
        ts.ajax.register(DictWidget.initialize, true);
    } else if (window.bdajax !== undefined) {
        bdajax.register(DictWidget.initialize, true);
    } else {
        DictWidget.initialize();
    }
    register_array_subscribers();
});
