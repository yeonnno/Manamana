import Image from "next/image";

interface Props {
    tagName: string,
    deleteTag: (value: string) => void
}


export default function SearchTag(props: Props) {

    const ondeleteTagClick = () => {
        props.deleteTag(props.tagName);
    }

    return (
        <div className="flex justify-center items-center gap-2 bg-PrimaryLight text-FontPrimaryDark pl-2 pr-2 pt-1 pb-1 rounded-xl">
            <div className="inline-block">
                {props.tagName}
            </div>
            <div className="inline-block" onClick={ondeleteTagClick}>
                <Image
                    src={'/images/Delete_White.png'}
                    alt='delete tag'
                    width={8}
                    height={8}
                />
            </div>
        </div>
    );
};