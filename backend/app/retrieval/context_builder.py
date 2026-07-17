class ContextBuilder:

    @staticmethod
    def build(results):

        context = []

        for item in results:

            if hasattr(item, "page_content"):

                context.append(item.page_content)

            elif hasattr(item, "content"):

                context.append(item.content)

        return "\n\n".join(context)