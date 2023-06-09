import { useState } from 'react';
import SwipeableDrawer from '@mui/material/SwipeableDrawer';
import { MyChat } from './MyCommentList';
import CommentInput, { CommentUserInput } from '../comment/CommentInput';

interface ChatListModalProps {
  chat: MyChat;
  open: boolean;
  close: () => void;
  deleteComment: (ee: any) => void;
  modifyComment: (oldComment: MyChat, newComment: MyChat) => Promise<boolean>;
}

function MyCommentListModal({
  chat,
  open,
  close,
  deleteComment,
  modifyComment,
}: ChatListModalProps) {
  const [modalState, setModalState] = useState<string>('init');

  const openModal = () => {};
  const closeModal = () => {
    close();
    setModalState('init');
  };

  const changeModalState = (e: string) => {
    setModalState(e);
  };
  const deleteChat = () => {
    deleteComment(chat);
    closeModal();
  };
  const modifyChat = async (e: CommentUserInput) => {
    const oldComment = chat;
    const newComment = {
      id: chat.id,
      content: e.content,
      createTime: chat.createTime,
      isSpoiler: e.spoiler,
      webtoon: {
        id: chat.webtoon.id,
        name: chat.webtoon.name,
        imagePath: chat.webtoon.imagePath,
      },
    };
    const result = await modifyComment(oldComment, newComment);
    closeModal();
    return result;
  };

  const popupDelete = (
    <div className="flex justify-center">
      <div className="my-6 flex w-2/3 flex-col items-center justify-center">
        <p className="text-center text-2xl text-PrimaryLight">이 댓글을 정말 삭제하시겠습니까?</p>
        <hr className="my-2 w-full border border-PrimaryLight bg-PrimaryLight" />
        <button
          className="flex w-1/2 flex-col items-center justify-center py-3"
          onClick={deleteChat}
        >
          <p className="text-center">삭제하기</p>
        </button>
      </div>
    </div>
  );

  const popupModify = (
    <div className="flex justify-center">
      <div className="my-6 flex w-[80%] flex-col items-center justify-center">
        <p className="text-center text-2xl text-PrimaryLight">리뷰 수정</p>
        <hr className="my-2 w-full border border-PrimaryLight bg-PrimaryLight" />
        <CommentInput
          defaultValue={{ content: chat.content, spoiler: chat.isSpoiler }}
          comment={modifyChat}
        />
      </div>
    </div>
  );

  const popupListForUser = (
    <div className="flex justify-center">
      <div className="my-6 flex w-2/3 flex-col items-center justify-center">
        <p className="text-center text-2xl text-PrimaryLight">댓글 설정</p>
        <hr className="my-2 w-full border border-PrimaryLight bg-PrimaryLight" />
        <button
          className="flex w-1/2 flex-col items-center justify-center py-3"
          onClick={() => {
            changeModalState('del');
          }}
        >
          <p className="text-center">삭제하기</p>
        </button>
        <button
          className="flex w-1/2 flex-col items-center justify-center py-3"
          onClick={() => {
            changeModalState('modify');
          }}
        >
          <p className="text-center">수정하기</p>
        </button>
      </div>
    </div>
  );

  const popupForUser = () => {
    if (modalState === 'init') {
      return popupListForUser;
    } else if (modalState === 'del') {
      return popupDelete;
    } else if (modalState === 'modify') {
      return popupModify;
    }
  };

  return (
    <SwipeableDrawer anchor={'bottom'} open={open} onOpen={openModal} onClose={closeModal}>
      {popupForUser()}
    </SwipeableDrawer>
  );
}

export default MyCommentListModal;
