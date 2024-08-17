var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.DBC_Button = function (props) {
    const {setData, data} = props;

    function onClick() {
        setData();
    }

    return React.createElement(
        window.dash_bootstrap_components.Button,
        {
            onClick,
            color: props.color,
            class_name: "my-1 py-1 px-2"
        },
        props.value
    );
};