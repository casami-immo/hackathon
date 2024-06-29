import gradio as gr

from backend.database import in_memory as db


with gr.Blocks() as demo:
    gr.Markdown("Virtual visit with Casami")

    with gr.Tab('Visitor interface'):
        # drop down to select property
        properties = db.get_properties()

        property_select = gr.Dropdown(
            [(property['name'], property['id']) for property in properties], 
            # value=(properties[0]['name'], properties[0]['id']),
            label="Select Property",
            interactive=True,
            multiselect=False)
        gr.Text(property_select.value)
        if property_select.value:
            property_id = property_select.value[0][1]
            views = db.get_views_by_property_id(property_id)        
            view = gr.Dropdown(
                [(view['name'], view['video']) for view in views],
                # value=(views[0]['name'], views[0]['video']),
                label="Select Room",
                multiselect=False, interactive=True)
            gr.Text(view.value[0][1], interactive=True)
            # gr.Video(view.choices[0][1], label="Virtual Visit", interactive=True)

if __name__ == '__main__':
    demo.launch()